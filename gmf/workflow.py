from gmf.tools.logger import setup_logger
from gmf.tools.config import read_config
import inspect
log = setup_logger()


class Workflow:
    
    
    def __init__(self, **options):
        
        self.modules     = []  # Store the modules added
        self.user_params = []
        
        self.compiled = False
        
    def _get_module_from_tag(self, tag):
        
        for module in self.modules:
            if module.tag == tag:
                return module
            
        raise Exception(f'Tried to reference module with tag {tag} but it does not exist in the workflow.')


    def add(self, module, tag, **kwargs):

        log.info(f'Adding module : {module.__name__}')
        self.modules.append(module(tag=tag, **kwargs))
        
        self.compiled = False


    def compile(self):
        
        log.info('-- Compiling Workflow --')
        
        for module in self.modules:

            log.info(f'     Inspecting module : {module.tag}')

            # Is an input module (requires user to provide arguments)
            if module.runtime_input:
                self.inspect_user_module(module)
                
                
            # Is a process module (requires inputs from other modules)
            else:
                self.inspect_internal_module(module)

        self.compiled = True

    def _get_pos_args(self, func, ignore=['self']):
        
        # Get the signature of the module's `run` method
        profile = inspect.signature(func)

        # Extract all parameters except 'self'
        positional_args = [
            param_name
            for param_name, param in profile.parameters.items()
            if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            and (param_name not in ignore)
        ]
        return positional_args


    def inspect_user_module(self, module):
        
        positional_args = self._get_pos_args(module.run)
        positional_args = [(module.tag, arg) for arg in positional_args]
        self.user_params.extend(positional_args)
        log.info(f'         Adding required user arguments : {[i[1] for i in positional_args]}')



    def inspect_internal_module(self, module):

        links = module.links
        
        positional_args = self._get_pos_args(module.run)
        
        for arg_name, link in links.items():

            if arg_name not in positional_args:
                raise ValueError(f'Argument "{arg_name}" is not a valid argument for module {module.tag}')

            if ':' not in link:
                raise ValueError(f'Link must be in the format of "module:arr"')

            tag, attr = link.split(':')           

            log.info(f'         Establishing link between : {module.tag}  -->  {tag}.{attr}')

            dependecy = self._get_module_from_tag(tag)

            if not hasattr(dependecy, attr):
                raise AttributeError(f'Module {dependecy.tag} does not have attribute "{attr}" (Check the expression "{link}")')

            
            
    def execute(self, **params):
        
        log.info('-- Executing Workflow --')      
        
        if self.compile == False:
            raise Exception('Workflow must be compiled before execution.')
        
        for module in self.modules:

            log.info('Running Module : ' + module.tag)    

            log.info(f'     Arguments : ')

            if module.runtime_input:
                
                opts = params.get(module.tag, {}) 
                
                for key, value in opts.items():
                    log.info(f'         {key.ljust(20)} : {str(value)}')
                
                module.run(**opts)
                    
            else:
                
                links = module.links
                
                kwargs = {}
                opts = params.get(module.tag, {}) 
            
                for arg_name, link in links.items():
                    
                    tag, attr = link.split(':')
                    
                    dependency = self._get_module_from_tag(tag)
                    
                    kwargs[arg_name] = getattr(dependency, attr)
                    
                for key, value in kwargs.items():
                    log.info(f'         {key.ljust(20)} : {str(type(value).__name__)}')
            
                kwargs = opts | kwargs
            
                # Run the module with the resolved dependencies
                module.run(**kwargs)
    