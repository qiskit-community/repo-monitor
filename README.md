[![Tests](https://github.com/qiskit-community/repo-monitor/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/qiskit-community/repo-monitor/actions/workflows/tests.yml)
[![Contributors][contributors-shield]][contributors-url]
[![Releases][releases-shield]][releases-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache 2.0][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
 <h3 align="center">Qiskit repo monitor</h3>

  <p align="center">
    Repository for automation of Qiskit issues and prs monitoring.
    <br />
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Repository for automation of Qiskit issues and prs monitoring.
All reports generated are stored in [project wiki](https://github.com/qiskit-community/repo-monitor/wiki).

<!-- USAGE EXAMPLES -->
## Usage

This is CLI application to generate issues report from specified repositories.

```shell
mkdir reports
python manager.py --token="<YOUR_GITHUB_TOKEN>" generate_reports_to_folder '["https://github.com/Qiskit/qiskit-finance"]'
```


<!-- ROADMAP -->
## Roadmap

See the [contributing](./CONTRIBUTING.md) document to learn about the source code contribution process quantum asset developers follow.

See the [code of conduct](./CODE_OF_CONDUCT.md) to learn about the social guidelines quantum developers are expected to adhere to.

See the [open issues](https://github.com/qiskit-community/repo-monitor/issues) for a list of proposed features (and known issues).



<!-- LICENSE -->
## License

Distributed under the Apache License. See [LICENSE.txt](./LICENSE) for more information.




<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/static/v1?label=CONTRIBUTORS&message=2&color=blue
[contributors-url]: https://github.com/qiskit-community/repo-monitor/graphs/contributors
[releases-shield]: https://img.shields.io/static/v1?label=RELEASES&message=0&color=purple
[releases-url]: https://github.com/qiskit-community/repo-monitor/releases
[stars-shield]: https://img.shields.io/static/v1?label=STARS&message=2&color=red
[stars-url]: https://github.com/qiskit-community/repo-monitor/stargazers
[issues-shield]: https://img.shields.io/static/v1?label=ISSUES&message=4&color=orange
[issues-url]: https://github.com/qiskit-community/repo-monitor/issues
[license-shield]: https://img.shields.io/static/v1?label=LICENSE&message=Apache2.0&color=green
[license-url]: https://github.com/qiskit-community/repo-monitor/blob/main/LICENSE
