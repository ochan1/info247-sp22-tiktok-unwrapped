source .venv\\Scripts\\activate

counter=0
step=100
cap=78286
while [ $counter -lt $cap ]
do
   py .\\scraping.py $counter $step || exit 1
   counter=$(( $counter + $step + ($counter == 0 ? 1 : 0) ))
done
echo "$counter"
