#### Project

`ec2_management`

#### Description

Launch ,start ,stop ,reboot and terminate ec2 instances using python-boto3 sdk.

#### Initial setup

`
aws sdk configured with IAM role with EC2 full access policy.
`

#### Usage

Returns dictionary.

```
from ec2_management.cssrt import create_ec2_instances

pprint(create_ec2_instances(region='us-west-1',
                            root_vol_size=30,
                            lvm_vol_size=20, #is for adding a data disk.
                            tmp_vol_size=15,
                            no_of_instances=1, #checks if its within 10 instances else fails.
                            name='NEW',
                            instance_type='t2.medium',
                            iam_arn='arn:aws:iam::xxxxxxxxx:instance-profile/xxxxxxx'))

```




