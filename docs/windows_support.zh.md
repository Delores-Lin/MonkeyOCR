# 使用 WSL2 + Docker Desktop 运行
[En](./windows_support.md) | [Zh](./windows_support.zh.md)
## 安装WSL2 和Docker Desktop
首先，确保你的Windows版本支持WSL2
1. 启用WSL  
   管理员权限启动PowerShell
    * 开启虚拟机平台功能
    ```PowerShell
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
    ```
    * 开启WSL
    ```PowerShell
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    ```
    * 重启电脑

2. 安装Linux发行版
   ```PowerShell
   wsl --install -d Ubuntu
   ```

3. 下载Docker Desktop  
   [Docker官网](https://www.docker.com/products/docker-desktop/)

4. 设置WSL config（可选）   
   如果后续需要量化模型，肯能会出现内存不够用的情况
    * 打开用户文件夹  
        在文件资源管理器中输入`%UserProfile%`回车
    * 创建一个`.wslconfig`文件
    * 用代码编辑器编辑文件内容
    ```.wslconfig
    [wsl2]
    memory=24GB
    ```
    其他参数可自行设置

## 构建容器
1. 运行Docker Desktop
2. 进入WSL
    ```PowerShell
    wsl
    cd ~
    ```
3.  克隆仓库
    ```PowerShell
    git clone https://github.com/Yuliang-Liu/MonkeyOCR

    cd MonkeyOCR
    ```
4.  按照README.md文件中的Docker Deployment创建Docker image  
    国内使用docker下载内容可能会比较慢，要考虑使用镜像

5. 进入container后就可以正常运行MonkeyOCR了  
   可以用vscode的`Dev Container`插件连接container，方便编辑修改

6. 如果你遇到`RuntimeError: No enough gpu memory for runtime.`表明显存不足，你可以尝试量化模型  
   详见 [量化方法](Quantization.zh.md)