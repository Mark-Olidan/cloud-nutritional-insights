from azure.storage.blob import BlobServiceClient

connect_str = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

try:
    container_client = blob_service_client.create_container("datasets")
    print("Container datasets created.")
except:
    container_client = blob_service_client.get_container_client("datasets")
    print("Container datasets already exists.")

with open("All_Diets.csv", "rb") as data:
    blob_client = container_client.get_blob_client("All_Diets.csv")
    blob_client.upload_blob(data, overwrite=True)
    print("All_Diets.csv uploaded to Azurite successfully.")