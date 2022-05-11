source .venv\\Scripts\\activate

counter=0
step=1000
cap=78286
while [ $counter -lt $cap ]
do
   # Echo the command as a checking ... if you change
   #  this line, make sure it's the same on the other
   echo "py .\\scraping.py $counter || exit 1"
   counter=$(( $counter + $step + ($counter == 0 ? 1 : 0) ))
done
echo "$counter"
