# The name of the container you want to remove
container_name="influxdb"

# Stop the container
docker stop $container_name

# Remove the container
docker rm $container_name

# List all volumes and find the ones associated with the container
for volume in $(docker volume ls -q); do
    # Check if the volume is associated with the container
    if docker volume inspect $volume | grep -q "$container_name"; then
        # Remove the volume
        docker volume rm $volume
    fi
done

rm -r ./python_environment
