# 使用AWQ进行量化
[En](./Quantization.md) | [Zh](./Quantization.zh.md)
1. 安装所需要的包
    ```bash
    pip install datasets
    ```

2. 在terminal中输入
    ```bash
    lmdeploy lite auto_awq \
        ./model_weight/Recognition \
        --calib-dataset 'ptb' \
        --calib-samples 64 \
        --calib-seqlen 1024 \
        --w-bits 4 \
        --w-group-size 128 \
        --batch-size 1 \
        --work-dir ./monkeyocr_quantization
    ```
    等待量化完成
    * 如果出现量化进程被killed，需要检查内存是否充足
    * 该参数的量化最大显存占用约为6.47G，以供参考

3.  你可能会出现以下报错
    ```
    RuntimeError: Error(s) in loading state_dict for Linear:
        size mismatch for bias: copying a param with shape torch.Size([2048]) from checkpoint, the shape in current model is torch.Size([1280]).
    ```
    这是由于你安装的LMDeploy版本还未适配Qwen2.5VL，需要前往GitHub仓库安装最新开发版
    ```bash
    pip install git+https://github.com/InternLM/lmdeploy.git
    ```
    安装完之后再次尝试量化

4.  量化完成后替换Recognition文件夹
    ```bash
    mv model_weight/Recognition Recognition_backup

    mv monkeyocr_quantization model_weight/Recognition
    ```
    再次尝试运行即可