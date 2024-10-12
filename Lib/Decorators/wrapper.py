# import time
# import inspect


# def _timing(func):
# 	run = True

# 	def wrapper(*args):
# 		start_time = time.time()
# 		result = func(*args)
		
# 		if run == True:
# 			end_time = time.time()
# 			elapsed_time = end_time - start_time
# 			print(f'Running time {func.__name__}:', round(elapsed_time, 4), 'second')	
			
# 		return result
		
# 	return wrapper



# import functools
# import inspect


# global_print_on = True

# def _log_input_output(print_on=False):
# 	def decorator(func):
# 		@functools.wraps(func)
# 		def wrapper(self, *args, **kwargs):
# 			result = func(self, *args, **kwargs)

# 			if print_on and global_print_on:
# 				object_name = None

# 				for i in inspect.currentframe().f_back.f_locals.items():
# 					if id(self) == id(i[1]):
# 						object_name = i[0]	

# 				if 	object_name == 'self':
# 					if self.name != None:
# 						object_name = self.name

# 				func_name = func.__name__

# 				arg_names = inspect.signature(func).parameters.keys()
# 				arg_values = {name: value for name, value in zip(list(arg_names)[1:], args)}
# 				arg_values.update(kwargs)
# 				input_params = ', '.join([f'{name}: {value}' for name, value in arg_values.items()])
				
# 				output_result = result
			
# 				print(f'Object: {object_name}, Function: {func_name}, Input params: {input_params}, Output result: {output_result}')
# 			else:
# 				print('')

# 			return result
# 		return wrapper
# 	return decorator




import time
import functools
import inspect


def _timing(print_log):
	global_print_log = True

	def decorator(func):
		@functools.wraps(func)
          
		def wrapper(*args, **kwargs):
			start_time = time.time()
            
			result = func(*args, **kwargs)
			
			if print_log and global_print_log:	
				end_time = time.time()
				elapsed_time = end_time - start_time
				print(f'Running time {func.__name__}:', round(elapsed_time, 4), 'second')
			
			return result
		return wrapper
	return decorator 


def _log_input_output(print_log):
    global_print_log = True
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if print_log and global_print_log:
                object_name = None

                if len(args) > 0 and isinstance(args[0], object):
                    for i in inspect.currentframe().f_back.f_locals.items():
                        if id(args[0]) == id(i[1]):
                            object_name = i[0]

                if object_name == 'self':
                    if args[0].name != None:
                        object_name = args[0].name

                func_name = func.__name__

                arg_names = inspect.signature(func).parameters.keys()
                arg_values = {name: value for name, value in zip(list(arg_names), args)}
                arg_values.update(kwargs)
                input_params = ', '.join([f'{name}: {value}' for name, value in arg_values.items()])

                output_result = result

                print(f'Object name: {object_name}, Function: {func_name}, INPUT PARAMETRS: {input_params}, OUTPUT RESULT: {output_result}')


            return result
        return wrapper
    return decorator