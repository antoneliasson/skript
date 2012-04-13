#!/bin/bash
#
# Skriptet förutsätter att programmet lftp är installerade, samt att
# användarens ~/.netrc är konfigurerad.

# Domännamn eller IP-adress till FTP-servern:
server='test.antoneliasson.se'

# Skapa fil som kommer att innehålla kommandon att köra
cmdfile=$(mktemp)

# Försök hämta lista med kommandon från servern. Ta bort källfilen (från servern) efter lyckad hämtning.
if (lftp -e "set xfer:clobber true; get -E remote.cmds -o $cmdfile; exit" $server); then
    # Skapa loggfil
    logfile=$(mktemp)
    
    while read cmd; do
        echo "$(date '+[%F %T]') $ $cmd" | tee -a $logfile
        bash -c "$cmd" 2>&1 | tee -a $logfile
#        echo "Status: $?" | tee -a $logfile # funkar vanligtvis inte
    done < $cmdfile
    
    # Kolla klockan för filnamnet
    timestamp=$(date '+%Y%m%d_%H%M%S')
    
    # Skicka loggen till servern. Ta bort källfilen (från disk) efter lyckad överföring.
    lftp -e "put -E $logfile -o remote-$timestamp.log; exit" $server
    
    # Spara loggen lokalt om den är kvar
    if [[ -f $logfile ]]; then
        mv $logfile ~/remote-$timestamp.log
    fi
fi

# Ta bort kommandofilen
rm $cmdfile

# Återställ variabler
unset server cmdfile logfile

