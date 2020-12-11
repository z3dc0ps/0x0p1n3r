#!/bin/bash
#Coded-by Jimmi Simon
#version=V1.5

NC='\033[0m'
Green='\033[0;32m'
if [[ $1 == "-u" ]]
then
        cd ../;
	sudo rm -r 0x0p1n3r ; 
	git clone https://github.com/z3dc0ps/0x0p1n3r ; 
	printf "\n\n ${Green} run : cd ../0x0p1n3r ; dos2unix ./*"

elif [[ $1 == "" ]]
then
        export PATH=$PATH:$(go env GOPATH)/bin
	
	printf "
			  ___        ___        _       _____      
			 / _ \__  __/ _ \ _ __ / |_ __ |___ / _ __ 
			| | | \ \/ / | | | '_ \| | '_ \  |_ \| '__|
			| |_| |>  <| |_| | |_) | | | | |___) | |   
			 \___//_/\_\____/| .__/|_|_| |_|____/|_|   
			                 |_|                       

					V1.5
			Developed By : Jimmi Simon\n"
	
	printf "\nEnter the Domain : "
	domain=`python3 tools/domain.py`

	if [[ $domain == *http://* ]] || [[ $domain == *https://* ]];
	then
		echo "Enter Domain without http/https "
		exit
	else
		cp config.json tools/knock/knockpy/
		printf "\nDomain is $domain , Searching for Subdomains"
		printf "\nThis may take a while...\n"
	
	
		if [ -f temp.txt ]; then
	   		sudo rm temp.txt
	   	fi
		if [ -f $domain ]; then
		   	sudo rm $domain
		fi
		if [ -f $domain"new" ]; then
	   		sudo rm $domain"new"
	   	fi
	
		sub=`amass enum -passive -d $domain -o temp.txt  -silent`
		echo "5% completed..."
		sub1=`assetfinder --subs-only $domain | sort -u | tr " " "\n" >> temp.txt`
		echo "10% Completed..."
		sub2=`gau -subs $domain | cut -d / -f 3 | cut -d ":" -f1 | tr " " "\n" | sort -u >> temp.txt`
		echo "15% Completed..."
		sub3=`python3 tools/knock/knockpy/knockpy.py $domain | cut -d "," -f1  | tr "]" " "| tr '"' " " | tr "[" " "  | cut -d " " -f6 >>temp.txt`
		echo "25% Completed..."
		sub4=`python3 tools/Sublist3r/sublist3r.py -d $domain -n >> temp.txt`
		echo "30% Completed..."
		sub5=`python3 tools/SUB-Z/Sub-Z.py -d $domain | cut -d "/" -f3 >> temp.txt`
		echo "40% Completed..."
		sub6=`python3 tools/V1D0m/v1d0m.py -d $domain >> temp.txt`
		echo "45% Completed..."
		sub7=`http "https://crt.sh/?q=%25.$domain&output=json" | jq -r .[].name_value | sed 's/\*\.//g' | httpx -title -silent | anew | cut -d " " -f1 | sort -u >> temp.txt`
		echo "50% completed..."
		sub8=`http "https://dns.bufferover.run/dns?q=.$domain" | jq -r .FDNS_A[] |cut -d "," -f2|sort -u >> temp.txt`
		echo "55% completed..."
		sub9=`http "https://riddler.io/search/exportcsv?q=pld:$domain" | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u >>temp.txt`
		echo "60% completed..."
		sub10=`http "http://web.archive.org/cdx/search/cdx?url=*.$domain/*&output=text&fl=original&collapse=urlkey" | sed -e 's_https*://__' -e "s/\/.*//" | cut -d ":" -f1 | sort -u >> temp.txt`
		echo "70% completed..."
		sub11=`http 'https://securitytrails.com/list/apex_domain/$domain' | grep -Po '((http|https):\/\/)?(([\w.-]*)\.([\w]*)\.([A-z]))\w+' | grep '.$domain' | sort -u >> temp.txt`
		echo "75% completed..."
		sub12=`http "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=$domain" | jq -r .subdomains[] >> temp.txt`
		echo "80% completed..."
		sub13=`http "https://api.hackertarget.com/hostsearch/?q=$domain" --body | cut -d "," -f1 >> temp.txt`
		echo "85% completed..."
		sub14=`http "https://sonar.omnisint.io/subdomains/$domain" --body | grep "$domain" | sed 's/"//g' | sed 's/,//g' | sed 's/ //g' | sort -u >> temp.txt`
		echo "90% completed..."
		findomain -t $domain | httprobe >> $domain"new"
		echo "subdomain enumeration completed.."
		
		
		sort -u temp.txt> $domain
		sudo rm temp.txt
	
		echo "checking live sub-domains.."
		fin=`cat $domain | httprobe  >> $domain"new"`
	
		echo "sorting..."
		sort -u $domain"new"> $domain
		echo "100% completed"
		sudo rm $domain"new";

		printf "\n     ${Green}Result Saved in $domain ${NC}\n\n";
		read -p "Do you want to check Subdomain Takeover y/n : " check

		if [[ $check == "n" || $check == "N" ]];then
			exit;
		
		elif [[ $check == "y" || $check == "Y" ]]; then

			printf "\nChecking for subdomain takeover,This may take a while...\n"
			python3 tools/takeover/takeover.py -l $domain

		else
			echo "Enter Correct option"
		fi

	fi
else
        echo "Enter Correct Option";
        printf "${Green} Usage : bash run.sh\n";
        printf "${Green} Update: bash run.sh -u \n";

fi


