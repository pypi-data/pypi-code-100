import json

from google.protobuf.json_format import Parse, MessageToJson

import fit_fill_pb2 as pb
import fit_fill_pb2_grpc as pb_rpc
import locapip


def _pass(*args, **kwargs):
    pass


if locapip.server is not None:
    mesh_reset = {'DynamicBody': _pass, 'StaticBody': _pass}
    mesh_add_point = {'DynamicBody': _pass, 'StaticBody': _pass}
    mesh_add_face = {'DynamicBody': _pass, 'StaticBody': _pass}
    mesh_build = {'DynamicBody': _pass, 'StaticBody': _pass}


    def simulate(message):
        return '{}'


    def simulate_result(message):
        return '{}'


    class Service(pb_rpc.FitFillServicer):
        async def upload_mesh(self, request_iterator, context):
            name = ''
            point_num = 0
            face_num = 0
            async for request in request_iterator:
                if request.WhichOneof('type') == 'name':
                    name = request.name
                    mesh_reset[name]()
                elif request.WhichOneof('type') == 'points':
                    for point in request.points.points:
                        if len(point.values) >= 3:
                            point_num += 1
                            mesh_add_point[name](tuple(point.values[:3]))
                elif request.WhichOneof('type') == 'faces':
                    for face in request.faces.faces:
                        if len(face.values) >= 3:
                            face_num += 1
                            mesh_add_face[name](tuple(face.values))
            mesh_build[name]()
            return pb.MeshInfo(point_num=point_num, face_num=face_num)

        async def simulate(self, request, context):
            return Parse(simulate(MessageToJson(request, True, True)), pb.Simulate())

        async def simulate_result(self, request, context):
            return Parse(simulate_result(MessageToJson(request, True, True)), pb.SimulateResult())


    pb_rpc.add_FitFillServicer_to_server(Service(), locapip.server)

else:
    import vtk


    async def upload_mesh(cpp_request):
        request_dict = json.loads(cpp_request(str()))

        reader = vtk.vtkSTLReader()
        reader.SetFileName(request_dict['path'])
        reader.Update()

        poly = reader.GetOutput()

        yield pb.Mesh(name=request_dict['name'])

        mesh = pb.Mesh()

        for i in range(poly.GetNumberOfPoints()):
            values = poly.GetPoint(i)
            mesh.points.points.append(pb.Vector(values=values))

            if len(mesh.points.points) > 37450 or i == poly.GetNumberOfPoints() - 1:
                print('upload', mesh.ByteSize(), 'bytes')
                yield mesh
                mesh = pb.Mesh()

        for i in range(poly.GetNumberOfCells()):
            ids = poly.GetCell(i).GetPointIds()
            values = [ids.GetId(i) for i in range(ids.GetNumberOfIds())]
            mesh.faces.faces.append(pb.Indices(values=values))

            if len(mesh.faces.faces) > 80660 or i == poly.GetNumberOfCells() - 1:
                print('upload', mesh.ByteSize(), 'bytes')
                yield mesh
                mesh = pb.Mesh()


    locapip.pb[__name__] = pb
    locapip.stub[__name__] = pb_rpc.FitFillStub

    locapip.py_request[__name__] = {
        'upload_mesh': upload_mesh,
        'simulate': pb.Simulate,
        'simulate_result': pb.SimulateResult,
    }

    locapip.py_response[__name__] = {
    }
