#!/bin/bash
#
# Skriptet förutsätter att programmen screen och lftp är installerade, samt att
# användarens ~/.netrc är konfigurerad.

# Domännamn eller IP-adress till FTP-servern:
server='test.antoneliasson.se'

# Skapa fil som kommer att innehålla kommandon att köra
cmdfile=$(mktemp)

# Försök hämta lista med kommandon från servern. Ta bort källfilen (från servern) efter lyckad hämtning.
if (lftp -e "set xfer:clobber true; get  remote.cmds -o $cmdfile; exit" $server); then
    # Starta en screen att köra kommandon i
    screen -d -m -S remote
    
    # Skapa loggfil
    logfile=$(mktemp)
    # Starta loggning
    screen -S remote -X logfile $logfile
    screen -S remote -X log on
    
    while read cmd; do
        echo $cmd;
        screen -S remote -X exec echo "$(date '+[%F %T]') $ $cmd"
        sleep 1
        screen -S remote -X exec $cmd
        sleep 1
        screen -S remote -X exec echo "Status: $?"
        sleep 1
    done < $cmdfile
    
    # Stoppa loggning
    screen -S remote -X log off
    # Avsluta screen
    screen -S remote -X kill
    
    # Kolla klockan för filnamnet
    timestamp=$(date '+%Y%m%d_%H%M%S')
    
    # Skicka loggen till servern. Ta bort källfilen (från disk) efter lyckad överföring.
    lftp -e "put  $logfile -o remote-$timestamp.log; exit" $server
    
    # Spara loggen lokalt om den är kvar
    if [[ -f $logfile ]]; then
        mv $logfile ~/remote-$timestamp.log
    fi
fi

# Ta bort kommandofilen
rm $cmdfile

# Återställ variabler
unset server cmdfile logfile

