


# vroid-dataset

This repo downloads the Vroid dataset introduced in [PAniC-3D: Stylized Single-view 3D Reconstruction from Portraits of Anime Characters](https://github.com/ShuhongChen/panic3d-anime-reconstruction)

This repo handles downloading only; for rendering, please use [vroid_renderer](https://github.com/ShuhongChen/vroid_renderer)


## download

First, download [`metadata.json`](https://drive.google.com/drive/folders/1KN58jhwA1Gf8UT5VoPkPiCI6WNtA9k2H?usp=sharing) to `./_data/lustrous/raw/vroid/`.  This json file contains all attributions for the 3D models used.  Then:

    # follow instructions in `./_env/vroid_cookie.bashrc` to get your cookie
    cp ./_env/vroid_cookie_template.bashrc ./_env/vroid_cookie.bashrc

    # build the container 
    docker-compose build

    # run the downloader
    bash ./run.sh


## citing

If you use our repo, please cite our work:

    @inproceedings{chen2023panic3d,
        title={Transfer Learning for Pose Estimation of Illustrated Characters},
        author={Chen, Shuhong and Zhang, Kevin and Shi, Yichun and Wang, Heng and Zhu, Yiheng and Song, Guoxian and An, Sizhe and Kristjansson, Janus and Yang, Xiao and Matthias Zwicker},
        booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
        year={2023}
    }


