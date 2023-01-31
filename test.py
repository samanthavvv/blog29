import wsgiref
from wsgiref.simple_server import make_server #,demo_ap

def demo_app(environ,start_response):
    """

    :param environ: wsgi server 会帮 appliction 收集服务端的属性存在此变量中；
    :param start_response: appliction 返回给客户端的状态码和响应头，通过参数传递给 start_response 函数，wsgi 会帮application解析并返回给客户端
    :return: application 返回给客户端的响应体body，通过return 返回。wsgi 会帮application 解析并传递给客户端
    """
    from io import StringIO		# 用于重定向标准输入/输出
    stdout = StringIO()
    print("Hello world!", file=stdout)	# 将输出重定向到stdout 这个对象中去
    print(file=stdout)
    h = sorted(environ.items())	#environ.items 收集服务端的一些属性
    for k,v in h:
        print(k,'=',repr(v), file=stdout)
    start_response("200 OK", [('Content-Type','text/plain; charset=utf-8')])
    return [stdout.getvalue().encode("utf-8")]	# 将收集了输出信息的重定向对象返回

ip='127.0.0.1'
port=9999
server = make_server(ip,port,demo_app)

server.serve_forever()
server.server_close()