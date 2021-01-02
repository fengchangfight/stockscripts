#!/bin/sh
trade_dates_file="/Users/xiefengchang/life/wealthmanagement/scripts/trade_dates.txt"

while IFS= read -r line
do
    echo "handling $line ..."
    python /Users/xiefengchang/life/wealthmanagement/scripts/stock_basic_info.py $line
    python /Users/xiefengchang/life/wealthmanagement/scripts/stock_bak_daily.py $line
    python /Users/xiefengchang/life/wealthmanagement/scripts/stockdaily.py $line
    python /Users/xiefengchang/life/wealthmanagement/scripts/industry_market_value.py $line
done < "$trade_dates_file"
