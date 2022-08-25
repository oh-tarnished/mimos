#!/bin/zsh

echo '\n█▀▄▀█ █ █▀▄▀█ █▀█ █▀'
echo '█░▀░█ █ █░▀░█ █▄█ ▄█    v0.0.1 \n'

# check if the argument is "ignite"
if [ "$1" = "ignite" ]; then
    echo "Starting the engine 🚀"
    # check if the argument is "help"
elif [ "$1" = "liftoff" ]; then
    echo "Initializing the engine 🚀\n"
    echo '[1/3] Checking compatibility of the system 🖥 ......'
# check if the os is windows
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "└── Detected linux"
        echo "  └── Detected Mac OSX\n"
        echo '[2/3] Installing required dependencies on your system......'     
        apt update && apt upgrade -y 
        echo '  └── Installing Python-3.10 ...\n'
                ## install python3.10 with apt 
                apt install python3.10 -y
                ## install python3.10 with pip
                pip3 install --upgrade pip

        # check if blender is installed
        if [ -f /usr/bin/blender ]; then
            echo '  └── Blender is already installed'
        else
            echo '  └── Installing Blender ...\n'
            ## install blender with apt
            apt install blender -y
            ## install blender with pip
            pip3 install blender
            # set path to blender
            export PATH=$PATH:/usr/bin/blender
        fi

        # check if miniconda is installed
        if [ -f /usr/bin/miniconda ]; then
            echo '  └── Miniconda is already installed'
        else
            echo '  └── Installing Miniconda 🐍...\n'
            ## install miniconda with apt
            apt install miniconda -y
            ## install miniconda with pip
            pip3 install miniconda
        fi        
        echo '[3/3] Getting you Started..... \n'
        echo '  └── Creating a miniconda environment with python 3.10...\n'
        conda create -n mimos python=3.10
        source activate mimos
        conda activate mimos
        # install the dependencies
        echo '  └── Installing the dependencies... on miniconda\n'
        pip install -r engine/requirements.txt
        echo 'Done and ready to go! 🚀'

elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  └── Detected Mac OSX\n"
        echo '[2/3] Installing required dependencies on your system......'     
        # check if homebrew is installed
        if ! command -v brew >/dev/null; then
                echo '  └── Installing homebrew...\n'
                /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        else
                echo '  └── Homebrew is already installed\n'
        fi
        echo '  └── Installing Python-3.10 ...\n'
                brew install python@3.10
        # check if blender is installed
        if ! command -v blender >/dev/null; then
                echo '  └── Installing blender...\n'
                brew install --cask blender
                # check if the current shell is zsh or bash
                if [[ $SHELL == *"zsh"* ]]; then
                        echo "alias blender=/Applications/Blender/blender.app/Contents/MacOS/blender" >> ~/.zshrc
                        source ~/.zshrc
                else
                       echo "alias blender=/Applications/Blender/blender.app/Contents/MacOS/blender" >> ~/.bash_profile
                       source ~/.bash_profile
                fi
        else
                echo '  └── Blender is already installed\n'
        fi
        echo '  └── Installing MiniConda 🐍 ...\n'
        #install miniconda if not installed
        if ! command -v conda >/dev/null; then
                wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh
                bash miniconda.sh -b -p $HOME/miniconda
                export PATH="$HOME/miniconda/bin:$PATH"
          else
             echo '  └── MiniConda 🐍 is already installed...\n'
            fi 
        echo '[3/3] Getting you Started..... \n'
        echo '  └── Creating a miniconda environment with python 3.10...\n'
        conda create -n mimos python=3.10
        source activate mimos
        conda activate mimos
        # install the dependencies
        echo '  └── Installing the dependencies... on miniconda\n'
        pip install -r engine/requirements.txt
        echo 'Done and ready to go! 🚀'

elif [[ "$OSTYPE" == "msys" ]]; then
        echo "└── Detected Windows"
else
    echo " └── Not supported OS 🛑"
    echo "Supported OS: Linux, Mac OSX"
    exit 1
fi

elif [ "$1" = "help" ]; then
    echo "help"
    # check if the argument is "version"

elif [ "$1" = "version" ]; then
    echo "version"

else
    echo "invalid argument\n "
    echo "usage: ./mimos.sh ignite | liftoff | help | version"
    echo "example: ./mimos.sh liftoff \n"
fi
