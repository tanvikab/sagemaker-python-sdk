#!/usr/bin/env python3

import boto3

def cleanup_endpoints():
    """Delete existing SageMaker endpoints and configurations."""
    sagemaker_client = boto3.client('sagemaker')
    
    # List all endpoints
    print("🔍 Finding existing endpoints...")
    endpoints = sagemaker_client.list_endpoints()
    
    for endpoint in endpoints['Endpoints']:
        endpoint_name = endpoint['EndpointName']
        status = endpoint['EndpointStatus']
        
        print(f"📍 Found endpoint: {endpoint_name} ({status})")
        
        if 'llama' in endpoint_name.lower():
            try:
                print(f"🗑️  Deleting endpoint: {endpoint_name}")
                sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
                print(f"✅ Endpoint {endpoint_name} deletion initiated")
                
                # Also delete the endpoint configuration
                print(f"🗑️  Deleting endpoint config: {endpoint_name}")
                sagemaker_client.delete_endpoint_config(EndpointConfigName=endpoint_name)
                print(f"✅ Endpoint config {endpoint_name} deleted")
                
            except Exception as e:
                print(f"❌ Error deleting {endpoint_name}: {e}")
    
    print("🎯 Cleanup complete!")

if __name__ == "__main__":
    cleanup_endpoints()