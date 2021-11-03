# -*-coding:utf-8-*-
import torchvision
import torch.nn as nn
import torchvision.models as models

'''
# class model_SimCLR(nn.Module):
#     def __init__(self, name, n_features, projection_dim):
#         super(model_SimCLR, self).__init__()
#         self.n_features = n_features
#         self.backbone = nn.Sequential(*list(self.get_resnet(name).children())[:-2])
#         self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
#         self.fc = nn.Sequential(nn.Linear(self.n_features, self.n_features), nn.ReLU(), nn.Linear(self.n_features, projection_dim))
#
#     def forward(self, x):
#         backbone_output = self.backbone(x)
#         avgpool_output = self.avgpool(backbone_output)
#         encoder_output = avgpool_output.view(avgpool_output.size(0), -1)
#         projector_output = self.fc(encoder_output)
#         return projector_output
#
#     def get_resnet(self, name, pretrained=False):
#         resnets = {"resnet18": torchvision.models.resnet18(pretrained=pretrained),
#                    "resnet50": torchvision.models.resnet50(pretrained=pretrained)}
#         if name not in resnets.keys():
#             raise KeyError(f"{name} is not a valid ResNet version")
#         return resnets[name]


# class model_BIDFC(nn.Module):
#     def __init__(self, name, projection_dim):
#         super(model_BIDFC, self).__init__()
#         self.backbone = nn.Sequential(*list(self.get_resnet(name).children())[:-2])
#         self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
#         self.fc = nn.Linear(512, projection_dim)
#
#     def forward(self, x):
#         backbone_output = self.backbone(x)
#         avgpool_output = self.avgpool(backbone_output)
#         encoder_output = avgpool_output.view(avgpool_output.size(0), -1)
#         projector_output = self.fc(encoder_output)
#         return projector_output
#
#     def get_resnet(self, name, pretrained=False):
#         resnets = {"resnet18": torchvision.models.resnet18(pretrained=pretrained),
#                    "resnet50": torchvision.models.resnet50(pretrained=pretrained)}
#         if name not in resnets.keys():
#             raise KeyError(f"{name} is not a valid ResNet version")
#         return resnets[name]

# class model_downstream(nn.Module):
#     def __init__(self, base_model, out_dim):
#         super(model_downstream, self).__init__()
#         self.out_dim = out_dim
#         self.backbone = self.get_resnet(base_model)
# 
#     def forward(self, x):
#         x = self.backbone(x)
#         return x
# 
#     def get_resnet(self, name, pretrained=False):
#         resnets = {"resnet18": torchvision.models.resnet18(pretrained=pretrained, num_classes=self.out_dim),
#                    "resnet50": torchvision.models.resnet50(pretrained=pretrained, num_classes=self.out_dim)}
#         if name not in resnets.keys():
#             raise KeyError(f"{name} is not a valid ResNet version")
#         return resnets[name]
'''

class BaseSimCLRException(Exception):
    """Base exception"""

class InvalidBackboneError(BaseSimCLRException):
    """Raised when the choice of backbone Convnet is invalid."""

class InvalidDatasetSelection(BaseSimCLRException):
    """Raised when the choice of dataset is invalid."""

class model_SimCLR(nn.Module):

    def __init__(self, base_model, out_dim):
        super(model_SimCLR, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=out_dim),
                            "resnet50": models.resnet50(pretrained=False, num_classes=out_dim)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), self.backbone.fc)

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)


class model_BIDFC(nn.Module):
    def __init__(self, base_model, out_dim):
        super(model_BIDFC, self).__init__()
        self.out_dim = out_dim
        self.backbone = self.get_resnet(base_model)

    def forward(self, x):
        x = self.backbone(x)
        return x

    def get_resnet(self, name, pretrained=False):
        resnets = {"resnet18": torchvision.models.resnet18(pretrained=pretrained, num_classes=self.out_dim),
                   "resnet50": torchvision.models.resnet50(pretrained=pretrained, num_classes=self.out_dim)}
        if name not in resnets.keys():
            raise KeyError(f"{name} is not a valid ResNet version")
        return resnets[name]


class model_SimFC(nn.Module):

    def __init__(self, base_model, out_dim):
        super(model_SimFC, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=out_dim),
                            "resnet50": models.resnet50(pretrained=False, num_classes=out_dim)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), self.backbone.fc)

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)


if __name__ == '__main__':
    from torchstat import stat

    model1 = model_SimCLR(base_model="resnet18", out_dim=128)
    model2 = model_BIDFC(base_model='resnet18', out_dim=10)
    model3 = model_SimFC(base_model='resnet18', out_dim=128)
    print(model1)
    print('-'*100)
    print(model2)
    print('-' * 100)
    print(model3)