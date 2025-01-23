ssh autoexpense mkdir -p /app
ssh autoexpense ls /app/.git
if [ $? -ne 0 ]; then
  ssh autoexpense git clone git@github.com:dypabo/autoexpense3.git /app
fi
ssh autoexpense "cd /app ; git checkout master ; git pull ;"

