
# VROID Scraper

  
  
  

## SETUP

  
  
  
  

### Setup & Execution


1. Log In To Vroid Hub Via Chrome.

2. Open Up Developer Console

3. Navigate Into Application Tab

4. Select Cookies In Left Tab

5. Select Hub.Vroid.com

6. Copy Contents Of '_vroid_session'

7. Update run.sh export variables.

8. Run run.sh

  
  

### Configuration Parameters For

#### Mode

Different Modes Of Operation

*scrape*, *crawl*, *download*

Scrape: `mode=s` Crawls for N models based on parameters and downloads them.

Crawl: `mode=c` Crawls for N models and saves their information into a JSON file.

#### Cookies

Sets the authentication cookie required to download models.

Cookie: `cookie=rndomcookietoken` Token extracted to access VRoid Hub.






### Known Issues:

1. Files Created By Docker Will Be Saved By The Configured Docker User.
For Some Users That Is Root, And May Require `chmod` and `chgrp` on the `.\data` and `.\files` folder.
2. Output Seems to not be printed as the container runs, this has to due with Dockers output processing. No imedieat solutions found.
3. 