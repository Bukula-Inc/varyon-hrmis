# from jinja2.utils import contextfunction
from controllers.utils import Utils
class Print_Format_HTML_Generator:
    def __init__(self):
        pass
    
    # @contextfunction
    def cell(self,value):
        return """
            <div class="tcell">
                <div class="table">
                    <div class="trow ">
                        <div class="tcell m-0 p-0 h-align-start">
                            <span class="content-title">{{key|replace('_', ' ')|title}}:</span>
                        </div>
                        <div class="tcell m-0 p-0  h-align-start">
                            <span>{value}</span>
                        </div>
                    </div>
                </div>
            </div>
        """
    
    
class HTML_Generator(Print_Format_HTML_Generator):
    def __init__(self):
        pass
    # @contextfunction
    def default_print_format(data):
        return super().cell("hello")