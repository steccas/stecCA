<h1 align="center">
  <br>
  <a href="https://github.com/Steccas/stecCA"><img src="https://raw.githubusercontent.com/Steccas/stecCA/main/img/logo.png" alt="StecCA" width="256"></a>
  <br>
    StecCA
  <br>
</h1>

<h4 align="center">An easy to deploy Certificate Authority using <a href="https://github.com/cloudflare/cfssl" target="_blank">CFSSL</a>, <a href="https://github.com/Netflix/lemur" target="_blank">Lemur</a> and <a href="https://www.docker.com/" target="_blank">Docker</a> magic!.</h4>

<br>

<p align="center">
  <a href="https://github.com/Steccas/stecCA/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/Steccas/stecCA.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/Steccas/stecCA/network/members"><img src="https://img.shields.io/github/forks/Steccas/stecCA.svg?style=for-the-badge"></a>
  <a href="https://github.com/Steccas/stecCA/issues">
      <img src="https://img.shields.io/github/issues/Steccas/stecCA.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/Steccas/stecCA/stargazers">
    <img src="https://img.shields.io/github/stars/Steccas/stecCA.svg?style=for-the-badge">
  </a>
  <a href="https://github.com/Steccas/stecCA/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Steccas/stecCA.svg?style=for-the-badge">
  </a>
  <a href="https://linkedin.com/in/lucasteccanella">
    <img src="https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555">
  </a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#getting-started">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#you-may-also-like">Related</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#support">Support</a> •
  <a href="#license">License</a>
</p>


<!-- ABOUT THE PROJECT -->
## About The Project
I needed

## Key Features

* Easy and fast deploy!
  - Thanks to docker and bash scripting deploying a fully working CA doesn't take hours anymore!
* Root CA and Intermediary CA
  - Root CA is not directly exposed, an Intermediate CA (signed by root) will be signing the user created certificates.
* Web Interface
  - Lemur provides an easy to use web interface to issue, manage and revoke certificates.
* Automation
  - Lemur provides various automated checks on certificates, some have already been enabled but many many more can be enabled depending on your needs.
* OSCP Responder
  - CFSSL Own OSCP responder has been set-up, including automatic updates.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

WIP

This is an example of how to list things you need to use the software and how to install them.
* prereq
  ```sh
  
  ```

### Installation

WIP

1. Clone the repo
   ```sh
   git clone 
   ```
2. Edit the config files
   ```sh
   
   ```
3. Stert the setup script
   ```sh
   
   ```

<!-- USAGE EXAMPLES -->
## Usage

WIP

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_


## Credits

This project uses the following technologies:

* [CFSSL](https://github.com/cloudflare/cfssl)
* [Lemur](https://github.com/Netflix/lemur)
* [Docker](https://www.docker.com/)
* [Bash](https://www.gnu.org/software/bash/)

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Support

WIP

## You may also like...

WIP

<!-- LICENSE -->
## License

Distributed under the GNU GPL V3 License. See [LICENSE](https://github.com/Steccas/stecCA/blob/main/LICENSE) for more information.

---

> [linktr.ee](https://linktr.ee/steccas) &nbsp;&middot;&nbsp;
> GitHub [@Steccas](https://github.com/Steccas) &nbsp;&middot;&nbsp;
> LinkedIn [Luca Steccanella](https://linkedin.com/in/lucasteccanella)


