import asyncio

from google.protobuf.json_format import Parse, MessageToJson

import locapip
import locapip_test_pb2 as pb
import locapip_test_pb2_grpc as pb_rpc


class Service(pb_rpc.TestServicer):
    async def unary_unary(self, request, context):
        print('---------- Test unary_unary ----------')
        print('server receive')
        print(MessageToJson(request, True, True))
        response = pb.Text(text=request.text.replace('request', 'response'))
        print('server send')
        print(MessageToJson(response, True, True))
        return response

    async def unary_stream(self, request, context):
        print('---------- Test unary_stream ----------')
        print('server receive')
        print(MessageToJson(request, True, True))
        for _ in range(3):
            response = pb.Text(text=request.text.replace('request', 'response') + f' stream {_ + 1}')
            print('server send')
            print(MessageToJson(response, True, True))
            yield response

    async def stream_unary(self, request_iterator, context):
        print('---------- Test stream_unary ----------')
        t = []
        async for request in request_iterator:
            t.append(request.text.replace('request', 'response'))
            print('server receive')
            print(MessageToJson(request, True, True))
        response = pb.Text(text=' '.join(t))
        print('server send')
        print(MessageToJson(response, True, True))
        return response

    async def stream_stream(self, request_iterator, context):
        print('---------- Test stream_unary ----------')
        t = []
        async for request in request_iterator:
            t.append(request.text.replace('request', 'response'))
            print('server receive')
            print(MessageToJson(request, True, True))
            response = pb.Text(text=' '.join(t))
            print('server send')
            print(MessageToJson(response, True, True))
            yield response


async def py_request_unary(cpp_request):
    request_message = Parse(cpp_request(str()), pb.Text())
    request_message.text = request_message.text.replace('cpp', 'py')
    print(f'client send')
    print(MessageToJson(request_message, True, True))
    return request_message


async def py_request_stream(cpp_request):
    while True:
        await asyncio.sleep(1)
        request_json_ = cpp_request(str())
        if len(request_json_) == 0:
            break
        request_message = Parse(request_json_, pb.Text())
        request_message.text = request_message.text.replace('cpp', 'py')
        print(f'client send')
        print(MessageToJson(request_message, True, True))
        yield request_message


async def py_response_unary(response_message, cpp_response):
    response_message.text = response_message.text
    print(f'client receive')
    print(MessageToJson(response_message, True, True))
    response_message.text = response_message.text.replace('py', 'cpp')
    cpp_response(MessageToJson(response_message, True, True))


async def py_response_stream(response_message_iterator, cpp_response):
    async for response_message in response_message_iterator:
        response_message.text = response_message.text
        print(f'client receive')
        print(MessageToJson(response_message, True, True))
        response_message.text = response_message.text.replace('py', 'cpp')
        cpp_response(MessageToJson(response_message, True, True))
    cpp_response(str())


if locapip.server is not None:
    pb_rpc.add_TestServicer_to_server(Service(), locapip.server)
else:
    locapip.pb[__name__] = pb
    locapip.stub[__name__] = pb_rpc.TestStub

    locapip.py_request[__name__] = {
        'unary_unary': pb.Text,
        'unary_stream': pb.Text,
        'stream_unary': pb.Text,
        'stream_stream': pb.Text,
    }

    locapip.py_request[__name__] = {
        'unary_unary': py_request_unary,
        'unary_stream': py_request_unary,
        'stream_unary': py_request_stream,
        'stream_stream': py_request_stream,
    }

    locapip.py_response[__name__] = {
        'unary_unary': py_response_unary,
        'unary_stream': py_response_stream,
        'stream_unary': py_response_unary,
        'stream_stream': py_response_stream,
    }
