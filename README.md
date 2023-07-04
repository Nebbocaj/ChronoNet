# ChronoNet

Live version of project: [khrono.space](khrono.space)

- [Site Source Code](./ChronoNet/)
- [Weekly Updates](./weekly_progress)
- [Bot Code](./bots/)
- [Presentation Materials](./presentation/)

The [deploy](deploy.sh) shell script is used to automate updating the AWS server.

---

## Connecting to AWS

Use the `aws.pem` file to connect to the AWS EC2 bucket. Passwords are disabled for the SSH port.

### Linux/Unix
- Change PEM file permissions to 600
  - this can be done using `sudo chmod 600 aws.pem`
  - AWS will not allow you to connect if the permissions are not 600
- use `ssh -i "aws.pem" ubuntu@khrono.space`

### Windows
- If using PuTTY you have to convert the PEM file to a PuTTy key
  - you can use the [PuTTY key generator](https://www.puttygen.com/)
- You can also use VSCode's [Remote-SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension
  - make sure to configure the SSH Configuration File with the IdentityFile field set to the PEM file's **absolute** path 
