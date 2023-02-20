import glob
import setuptools

setuptools.setup(
    name="blog",
    version="1.0.1",
    author="ada",
    author_email="ada@163.com",
    description="blog project",
    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=setuptools.find_packages(),  # ['blog', 'post', 'users', 'post.migrations', 'users.migrations']
    # 需要打包的python 单文件列表
    py_modules=["messages", "manage", "setup"], # 去掉.py
    # # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片、示例的html 文件等
    data_files=[
        ('blog29', glob.glob('templates/*.html', recursive=True) + ['requirements'])],
    package_data={'': ['*.html']},
    url="http://iswbm.com/",  # 项目主页
    python_requires='>=3.9',
)
