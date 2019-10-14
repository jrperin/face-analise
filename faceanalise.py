import boto3
import json

""" Funcao Lambda para analise das imagens
    jrperin - 2019-10-13
"""

s3 = boto3.resource('s3')
cliente = boto3.client('rekognition')

# Indexar as faces de uma unica imagem
def detecta_faces():
    faces_detectadas = cliente.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPORARIA',
        Image={
            'S3Object' : {
                'Bucket' : 'jrp-fa-imagens',
                'Name'   : '_analise.png',
            },
        },
    )
    return faces_detectadas

def cria_lista_faceId_detectadas(faces_detectadas):
    faceId_detectadas = []
    for imagens in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][imagens]['Face']['FaceId'])
    return faceId_detectadas


def compara_imagens(faceId_detectadas):
    resultado_comparacao = []
    for id in faceId_detectadas:
        resultado_comparacao.append(
            cliente.search_faces(
                CollectionId='faces',
                FaceId =id,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return resultado_comparacao

faces_detectadas = detecta_faces()
faceId_detectadas = cria_lista_faceId_detectadas(faces_detectadas)
resultado_comparacao = compara_imagens(faceId_detectadas)
#print(json.dumps(faces_detectadas, indent=4))
#print(faceId_detectadas)
print(json.dumps(resultado_comparacao, indent=4))
