


# vroid-dataset

This repo downloads the Vroid 3D models dataset introduced in [PAniC-3D: Stylized Single-view 3D Reconstruction from Portraits of Anime Characters](https://github.com/ShuhongChen/panic3d-anime-reconstruction).  As described in that repo, this downloader will add to `./_data/lustrous`


## download

Download the `vroid-dataset.zip` from the project's [drive folder](https://drive.google.com/drive/folders/1Zpt9x_OlGALi-o-TdvBPzUPcvTc7zpuV?usp=share_link), and merge it with this repo's file structure.  There should be a `./_data/lustrous/raw/vroid/metadata.json`, which the following commands will use to download the models.  Note that `metadata.json` also contains all vroid model attributions.

Then, get your Vroid hub cookie following these steps:

    1) login to https://hub.vroid.com/en/ on chrome
    2) open devtools (f12)
    3) go to Application > Cookies > https://hub.vroid.com/en/
    4) copy the value of `_vroid_session`
    5) replace the cookie value in `./_env/vroid_cookie.bashrc` with your new cookie:
    cp ./_env/vroid_cookie_template.bashrc ./_env/vroid_cookie.bashrc

Finally, build the container and run the scraper:

    # build the container 
    docker-compose build

    # run the downloader
    bash ./run.sh


## citing

If you use our repo, please cite our work:

    @inproceedings{chen2023panic3d,
        title={PAniC-3D: Stylized Single-view 3D Reconstruction from Portraits of Anime Characters},
        author={Chen, Shuhong and Zhang, Kevin and Shi, Yichun and Wang, Heng and Zhu, Yiheng and Song, Guoxian and An, Sizhe and Kristjansson, Janus and Yang, Xiao and Matthias Zwicker},
        booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
        year={2023}
    }

