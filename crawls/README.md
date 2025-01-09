# crawls

Acquire data for fine tuning, especially PDF.

Can run a single job in heritrix directly from the command line.

```
$ $HOME/opt/heritrix-3.4.0-20220727/bin/heritrix \
    -a admin:admin \
    -r 2024-04-SOZPHIL-TEST-7 \
    -j $HOME/code/miku/helpdesk/crawls
```

## 2024-04-SOZPHIL-TEST-7

* can be less polite to be faster

```
$ find 2024-04-SOZPHIL-TEST-7 -name "crawl.log" | xargs grep -c pdf
2024-04-SOZPHIL-TEST-7/20240402195300/logs/crawl.log:41
2024-04-SOZPHIL-TEST-7/20240402213424/logs/crawl.log:1361
```

About 1300 pdfs.

```
$ grep "application/pdf" 2024-04-SOZPHIL-TEST-7/20240402213424/logs/crawl.log | awk '{print $4}'  | wc -l
1330
```

Mostly irrelevant to the question.
