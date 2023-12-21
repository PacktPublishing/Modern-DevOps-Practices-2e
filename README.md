# Modern DevOps Practices - Second Edition

<a href="https://www.packtpub.com/product/modern-devops-practices-second-edition/9781805121824"><img src="https://content.packt.com/B19877/cover_image_small.jpg" alt="no-image" height="256px" align="right"></a>

This is the code repository for [Modern DevOps Practices - Second Edition](https://www.amazon.com/Modern-DevOps-Practices-applications-cutting-edge/dp/1805121820), published by Packt.

**Implement, secure, and manage applications on the public cloud by leveraging cutting-edge tools**

## What is this book about?
This book helps you learn about modern distributed apps that run in the cloud on an infinite scale using containers, their architecture, and benefits; how to implement them within your development life cycle; and run them in production using modern DevOps tools, practices, and techniques.

This book covers the following exciting features:
* Explore modern DevOps practices with Git and GitOps
* Master container fundamentals with Docker and Kubernetes
* Become well versed in AWS ECS, Google Cloud Run, and Knative
* Discover how to efficiently build and manage secure Docker images
* Understand continuous integration with Jenkins on Kubernetes and GitHub Actions
* Get to grips with using Argo CD for continuous deployment and delivery
* Manage immutable infrastructure on the cloud with Packer, Terraform, and Ansible
* Operate container applications in production using Istio and learn about AI in DevOps

If you feel this book is for you, get your [copy](amazon_link) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders. For example, ch10.

The code will look like the following:
```
import os
import datetime
from flask import Flask
app = Flask(__name__)
@app.route('/')
def current_time():
    ct = datetime.datetime.now()
    return 'The current time is : {}!\n'.format(ct)
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

```

**Following is what you need for this book:**
If you are a software engineer, system administrator, or operations engineer looking to step into the world of DevOps within public cloud platforms, this book is for you. Existing DevOps engineers will also find this book helpful as it covers best practices, tips, and tricks for implementing DevOps with a cloud-native mindset. Although no containerization experience is necessary, a basic understanding of the software development life cycle and delivery will help you get the most out of this book.

With the following software and hardware list you can run all code files present in the book (Chapter 1-15).
### Software and Hardware List
| Software required | OS required |
| ------------------------------------ | ----------------------------------- |
| Google Cloud Platform | Windows, macOS, or Linux |
| AWS | Windows, macOS, or Linux |
| Azure | Windows, macOS, or Linux |
| Linux VM | Ubuntu 18.04 LTS or later |


### Related products
* SAFe® for DevOps Practitioners [[Packt]](https://www.packtpub.com/product/safe-for-devops-practitioners/9781803231426) [[Amazon]](https://www.amazon.com/SAFe%C2%AE-DevOps-Practitioners-Implement-Continuous/dp/1803231424)

* Automating DevOps with GitLab CI/CD Pipelines [[Packt]](https://www.packtpub.com/product/automating-devops-with-gitlab-cicd-pipelines/9781803233000) [[Amazon]](https://www.amazon.com/Automating-DevOps-GitLab-Pipelines-efficient/dp/1803233001)

## Get to Know the Author
**Gaurav Agarwal**
Gaurav Agarwal is a Senior Cloud Engineer at ThoughtSpot with over a decade of experience as a seasoned Cloud and DevOps Engineer. Previously, Gaurav served as a Cloud Solutions Architect at Capgemini and Software Developer at TCS. With a distinguished list of certifications, including HashiCorp Certified Terraform Associate, Google Cloud Certified Professional Cloud Architect, Certified Kubernetes Administrator, and Security Specialist, he possesses an impressive technical profile. Gaurav's extensive background encompasses roles where he played pivotal roles in infrastructure setup, cloud management, and the implementation of CI/CD pipelines. His technical prowess extends to numerous technical blog posts and a published book, underscoring his commitment to advancing the field.

## Other books by the authors
* Modern DevOps Practices [[Packt]](https://www.packtpub.com/product/modern-devops-practices/9781800562387k) [[Amazon]](https://www.amazon.com/Modern-DevOps-Practices-cutting-edge-techniques-ebook/dp/B097DQNQZ3?ref_=ast_author_mpb)

