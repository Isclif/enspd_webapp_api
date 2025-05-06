import uuid

number = 20

uuids = []
# i = 1

for i in range(number):
    generated_uuid = uuid.uuid4()
    generated_uuid = str(generated_uuid).replace("-", "")
    uuids.append(generated_uuid)

    print(generated_uuid)

    # i = i + 1

print(uuids)