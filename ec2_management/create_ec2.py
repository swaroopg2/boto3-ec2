try:
    import boto3
    import configparser
except ImportError:
    print("Installing required modules\n")
    import os
    os.system('python -m pip install boto3 configparser')

import boto3
import pprint
import configparser

'''
To avoid abuse of AWS resources ValueError is raised when no_of_instances exceeds more than 10
Check your limit settings in AWS and change accordingly.
'''


def create_ec2_instances(region='us-west-2', root_vol_size=20, lvm_vol_size=50, tmp_vol_size=10,
                         no_of_instances=1, name='NEW', instance_type='m5a.xlarge',
                         iam_arn='arn:aws:iam::xxxxxxxxx:instance-profile/xxxxxxx'):
    if no_of_instances > 10:
        raise ValueError

    config = configparser.ConfigParser()
    configfile = './ec2_management/variables.ini'
    config.read(configfile)
    subnet_id = config.get(region, "subnet_id")
    default_security_group_id = config.get(region, "sg_id")
    keypair = config.get(region, "keypair")
    ami_id = config.get(region, "ami_id")
    client = boto3.client("ec2", region_name=region)
    response = client.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': root_vol_size
                }
            },
            {
                'DeviceName': '/dev/xvdk',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': tmp_vol_size
                }
            },
            {
                'DeviceName': '/dev/sdb',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeType': 'gp2',
                    'VolumeSize': lvm_vol_size
                }
            },
        ],
        ImageId=ami_id,
        InstanceType=instance_type,
        SecurityGroupIds=[
            default_security_group_id,
        ],
        SubnetId=subnet_id,
        UserData='file:///user_data.txt',
        KeyName=keypair,
        MinCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': name
                    }
                ]
            },
        ],
        MaxCount=no_of_instances,
        IamInstanceProfile={
            'Arn': iam_arn,
        },
        InstanceInitiatedShutdownBehavior='stop'
    )
    return response


#Uncomment to create an EC2 node with provided config details
#Check your configs in variables.ini
# pprint(create_ec2_instances(region='us-west-1',
#                             root_vol_size=30,
#                             lvm_vol_size=20,
#                             tmp_vol_size=15,
#                             no_of_instances=11,
#                             name='NEW',
#                             instance_type='t2.medium',
#                             iam_arn='arn:aws:iam::xxxxxxxxx:instance-profile/xxxxxxx'))