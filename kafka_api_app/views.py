from django.shortcuts import render
import random
from .seriailizer import *
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,UpdateAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from confluent_kafka import Producer, Consumer, KafkaException
from .models import KafkaData


class KafkaAPIView(APIView):
    bootstrap_servers = 'localhost:9093'
    topic = 'api_data1'

    producer_config = {'bootstrap.servers': bootstrap_servers}
    producer = Producer(producer_config)

    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'latest'
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])

    def post(self, request, *args, **kwargs):
        try:
            for i in range(1, 100):
                data_to_send = {
                    "latitude": random.uniform(-90, 90),
                    "longitude": random.uniform(-180, 180),
                               }
                self.producer.produce(self.topic, key=None, value=str(data_to_send))
                self.producer.flush()

                # Consume data from Kafka
                msg = self.consumer.poll(10)  # Adjust the timeout as needed
                if msg is not None:
                    received_data = msg.value().decode('utf-8')
                else:
                    received_data = "No data received from Kafka."

                print(received_data)

                # Save data to MongoDB
                kafka_data = KafkaData(latitude=data_to_send['latitude'], longitude=data_to_send['longitude'], id= "RID" + str(i))
                kafka_data.save()

            return Response({'status': 'success',
                            'response code': status.HTTP_200_OK})

        except KafkaException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetData( GenericAPIView ):
    serializer_class = DataSerializer

    def get(self, request, pk, **kwargs):
        model = KafkaData.objects.get( pk=pk )
        serializer_class = self.serializer_class( model )
        return Response( serializer_class.data )


class UpdateData( GenericAPIView ):
    serializer_class = DataSerializer

    def put(self, request, pk):
        try:
            query_set = KafkaData.objects.get( pk=pk )
            serializer_class = self.serializer_class( instance=query_set, data=request.data )
            if serializer_class.is_valid():
                serializer_class.save()
                return Response( serializer_class.data )
        except Exception as e:
            print( 'invalid' )
            return Response( {"error": str( e )} )


class DeleteData( GenericAPIView ):
    def delete(self, request, pk):
        try:
            data = KafkaData.objects.get( pk=pk )
            data.delete()
            return Response( {"message": "deleted"} )
        except Exception as e:
            print( "invalid", e )
            return Response( {"error": str( e )} )

# class GetData(RetrieveAPIView):
#     serializer_class = IdSerializer
#
#     def get(self, request,**kwargs):
#         model = KafkaData.objects.get(id=request.data['id'])
#         serializer_class = DataSerializer(instance=model,data=request.data)
#         return Response(serializer_class.data)
#
#
# class UpdateData(UpdateAPIView):
#     serializer_class = DataSerializer
#
#     def put(self, request, *args, **kwargs):
#         try:
#             query_set = KafkaData.objects.get(id=request.data['id'])
#             serializer_class = DataSerializer(instance=query_set, data=request.data)
#             if serializer_class.is_valid():
#                 serializer_class.save()
#                 return Response(serializer_class.data)
#         except Exception as e:
#             print('invalid')
#             return Response({"error": str(e)})
#
#
# class DeleteData(GenericAPIView):
#     def delete(self, request, pk):
#         try:
#             patient = KafkaData.objects.get(pk=pk)
#             patient.delete()
#             return Response({"message": "deleted"})
#         except Exception as e:
#             print("invalid", e)
#             return Response({"error": str(e)})
