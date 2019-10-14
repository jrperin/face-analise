import boto3

""" Indexa as imagens no Rekognition
    jrperin - 2019-10-13
"""

s3 = boto3.resource('s3')
cliente = boto3.client('rekognition')

def lista_imagens():
    imagens=[]
    bucket = s3.Bucket('jrp-fa-imagens')
    for imagem in bucket.objects.all():
        imagens.append(imagem.key)
    return imagens

def indexa_colecao(imagens):
    for i in imagens:
        response = cliente.index_faces(
            CollectionId='faces',
            DetectionAttributes=[
            ],
            ExternalImageId=i[:-4],
            Image={
                'S3Object' : {
                    'Bucket' : 'jrp-fa-imagens',
                    'Name'   : i,
                },
            },
        )

imagens = lista_imagens()
indexa_colecao(imagens)