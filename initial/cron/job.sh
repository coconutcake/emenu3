echo "\nCron wykonuje zadanie: Wysyłka maili"
curl -X POST -k -s https://nginx:4433/commands/email_push/ -d '{"key":"20011865a6a3a79c47e5fa3b4dd31ba9c490186d"}' -H 'Content-Type: application/json' -H 'Accept: application/json' 
echo "KONIEC\n"
