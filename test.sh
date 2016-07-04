python draw.py test 3 blue > test.svg
if diff test.svg test/reference.svg
then
    echo "OK"
    rm test.svg
else
    echo "test ERROR"
fi
