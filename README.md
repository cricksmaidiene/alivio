# Alivio 🛖

> Building classification for natural disaster relief efforts

![](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)
![](https://img.shields.io/badge/Anaconda-44A833.svg?style=for-the-badge&logo=Anaconda&logoColor=white)
![](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![](https://img.shields.io/badge/Git-F05032.svg?style=for-the-badge&logo=Git&logoColor=white)
![](https://img.shields.io/badge/Amazon%20AWS-232F3E.svg?style=for-the-badge&logo=Amazon-AWS&logoColor=white)
![](https://img.shields.io/badge/Google%20Colab-F9AB00.svg?style=for-the-badge&logo=Google-Colab&logoColor=white)


- [Alivio 🛖](#alivio-)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
      - [Software](#software)
      - [Access Keys](#access-keys)
    - [Environment Setup](#environment-setup)
    - [Download \& Installation](#download--installation)
  - [Directory Structure](#directory-structure)

## Setup

### Prerequisites


#### Software

The following software should be pre-installed on the system using this repository:

* [`conda`](https://docs.anaconda.com/anaconda/install/index.html) or a virtual environment
* [`git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) for version control

#### Access Keys

Create the following keys if you don't have them

* [GitHub Developer Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) - to push and pull code to and from GitHub. This should be saved to the terminal or command line.
* [AWS IAM Credentials](https://k21academy.com/amazon-web-services/create-access-and-secret-keys-in-aws/) - to access AWS resources remotely.
    * Access Key
    * Secret Access Key

### Environment Setup

The following commands need to be run only once, during the initial setup process. 

* Create a conda environment
  * Create the environment (name `alivio` is optional and name can be used)

    ```bash
    conda create --name alivio python=3.10 -y
    ```

  * Activate the environment

    ```bash
    conda activate alivio
    ```

* Install poetry for python dependency management

  ```bash
  pip install poetry
  ```

* Configure AWS Credentials. This command will open up a terminal-based prompt with 4 inputs. 

  ```bash
  aws configure
  ```
  * Access Key: Your AWS Access Key
  * Secret Access Key: Your AWS secret access key
  * region: `us-east-1`
  * format: `json`


### Download & Installation

The following commands need to be run only once, during the initial setup process.

* Clone the GitHub repository

  ```bash
  git clone https://github.com/cricksmaidiene/alivio
  ```

* Visit the repository locally
  
  ```bash
  cd alivio
  ```

* Install the python dependencies

  ```bash
  poetry install --no-root
  ```

You can now start executing notebooks and code within this virtual environment.


## Directory Structure

* `/src`: for all source code and notebook files
  
  * `src/01_data_ingestion`: For notebooks and source related to ingesting raw data
  * `src/02_data_analysis`: For EDA, visualization and other analysis tasks
  * `src/03_data_engineering`: For preprocessing the dataset or performing feature engineering
  * `src/04_models`: For model training, fine-tuning and experimentation

* `/data`: For all data extracts saved locally
* `/docs`: For internal team documentation
* `/app`: For the web-interface


