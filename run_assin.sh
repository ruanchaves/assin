label="tmp_training_"
timestamp=$(date +%Y%m%d_%H%M%S)
DATE=$label$timestamp

if [[ $DATASET == 'assin2' ]]
then
    TEST_FILE='./sources/assin2-test.xml'
elif [[ $DATASET == 'assin-ptbr' ]]
then
    TEST_FILE='./sources/assin-ptbr-test.xml'
elif [[ $DATASET == 'assin-ptpt' ]]
then
    TEST_FILE='./sources/assin-ptpt-test.xml'
elif [[ $DATASET == 'toy' ]]
then
    TEST_FILE='./sources/toy-test.xml'
else
    exit 1
fi

cd /home
cd settings
python build_settings.py
cd ..

mkdir ../$DATE
rsync -avr --exclude="tmp_training_*" --exclude="submission_*" . ../$DATE
mv ../$DATE .
cd $DATE

python assin.py settings/settings.json
python final_submission.py

mkdir -p ./submission

echo 'ENSEMBLE : STACKING \n' >> ./submission/result.txt
python assin-eval.py  assin2-test.xml ./submission/submission-ensemble.xml >> ./submission/result.txt
echo 'ENSEMBLE : AVERAGE \n' >> ./submission/result.txt
python assin-eval.py  assin2-test.xml ./submission/submission-average.xml >> ./submission/result.txt

echo 'PORTUGUESE MODEL \n' >> ./submission/result.txt
python assin-eval.py  assin2-test.xml ./submission/submission-portuguese.xml >> ./submission/result.txt

echo 'ENGLISH MODEL \n' >> ./submission/result.txt
python assin-eval.py  assin2-test.xml ./submission/submission-english.xml >> ./submission/result.txt

# mv settings/settings.json ./submission/
# mv settings/config.yml ./submission/

# mkdir submission_$timestamp
# mv ./submission/* submission_$timestamp
# mv submission_$timestamp ..
# cd ..
# rm -rf $DATE