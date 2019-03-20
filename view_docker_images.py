import requests  
import json  
import traceback  
   
repo_ip = '124.126.15.123'  
repo_port = 5080  
   
def getImagesNames(repo_ip,repo_port):  
    docker_images = []  
    try:  
        url = "http://" + repo_ip + ":" +str(repo_port) + "/v2/_catalog"  
        res_dic =requests.get(url).json() 
        images_type = res_dic['repositories']  
        print(images_type)
        for i in images_type:  
            url2 = "http://" + repo_ip + ":" +str(repo_port) +"/v2/" + str(i) + "/tags/list"  
            res_dic2 =requests.get(url2).json() 
            name = res_dic2['name']  
            tags = res_dic2['tags']  
            for tag in tags:  
                docker_name = str(repo_ip) + ":" + str(repo_port) + "/" + name + ":" + tag  
                docker_images.append(docker_name)  
                print(docker_name)
    except:  
        traceback.print_exc()  
    return docker_images  
if __name__=='__main__':
       
    getImagesNames(repo_ip, repo_port) 
