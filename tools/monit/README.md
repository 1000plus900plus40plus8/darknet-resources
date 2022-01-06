Shout out to tutoriaLinux for their guide on monit 

https://www.youtube.com/watch?v=wiRt3mY7Rrw


## Does darknet randomly crash for you?
### Well the solution to your problem may be monit!

https://mmonit.com/monit/
Monit is a monitoring tool that can restart programs when they crash.

However, it can do more than just that, here is a copied and pasted statement f their website:
```
Monit is a small Open Source utility for managing and monitoring Unix systems.
Monit conducts automatic maintenance and repair and can execute meaningful causal actions in error situations.
```


# Monit quickstart (Linux)

1. Install monit from https://mmonit.com/wiki/Monit/Installation

This was a real pain for me but I was able to find a .deb file that worked for me here http://us.archive.ubuntu.com/ubuntu/pool/universe/m/monit/

Here are instructions for installing a .deb file http://us.archive.ubuntu.com/ubuntu/pool/universe/m/monit/

2. Enable the monit daemon `systemctl enable monit`
3. Start the monit daemon `systemctl start monit`

# Setting up monit to relaunch darknet on crash 
1. Create a backup of `/etc/monit/monitrc` file with the following command

`cp /etc/monit/monitrc /etc/monit/monitrc-original`
2. Copy the `monitrc-template` file from this folder to a working file `monitrc-working`

`cp monitrc-template monitrc-working`

This monitrc file is very similar to the basic monitrc that comes with a fresh installation file
I'll call out the changes I've made:
* Modify default timeout for service start since darknet takes some time to start
* Setup monit to launch Monit Service Manager on port 2818
* Add darknet (See step below for adding your training script!)

3. Locate your training script and get the **absolute path**. In this case I will use:
`/home/user/nn/example_network/example_network_train.sh`


4. Set a shell variable, `TRAINING_SCRIPT` to be equal to your absolute path of your training script

`TRAINING_SCRIPT=/home/user/nn/example_network/example_network_train.sh`

5. Replace the `TEMPLATE_REPLACE_ME_TEXT` placeholder text in your `monitrc-working` file using sed and the variable we defined above

`sed -i "s|TEMPLATE_REPLACE_ME_TEXT|$TRAINING_SCRIPT|g" monitrc-working`

Note that we use | here for a delimiter since our variable contains / characters
 
6Set monitrc permission to 600 

`chmod 600 monitrc-working`

7. Copy your `monitrc-working` file to `/etc/monit/monitrc` 

`sudo cp monitrc-working /etc/monit/monitrc`

8. Restart monit to load the new monitrc: 

`systemctl restart monit`

10. Open the Monit Service Manager http://localhost:2812/

Credentials are defined in the monitrc file
```
User = admin
Password = monit
```
You can find some more info on the Monit Service Manager in this video:
https://www.youtube.com/watch?v=3cA5lNje1Ow
11. Click on 'darknet' to view stats about the process - monit should automatically start this for you and relaunch it on crashes

# Ensuring darknet is running monit
To view logs:

`sudo tail -f /var/log/monit.log`

To check gpu usage:

`watch -d  nvidia-smi`

To check the output of darknet:

_Still working on this..._

# Why not make a script?
This post on stackoverflow to outlines why you shouldn't make a script for this and use a tool like Monit instead
https://stackoverflow.com/a/697064/7998814