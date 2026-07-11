
_IMPORT_MAPPING = {
    'make_blog_category': "helper_blogs",
    'make_blog_tag': 'helper_blogs',
    'make_blog_post': 'helper_blogs',
    'make_blog_section': 'helper_blogs',
    'make_car_description': 'helper_blogs',
    'make_car_description_section': 'helper_blogs',
    'make_brand_history': 'helper_blogs',
    'make_brand_history_section': 'helper_blogs',
}

def __getattr__(name:str):
    # Check if the called function/class is in the list
    if name in _IMPORT_MAPPING:
        import importlib
        
        # Get the corresponding module (file) name
        module_name = _IMPORT_MAPPING[name]
        
        full_module_path=f"blogs.tests.helpers.{module_name}"
        
        # Proceed to dynamically import that file
        module = importlib.import_module(full_module_path, __package__)
        
        # Take the function/class from that module and return it to the user
        attr = getattr(module, name)
        
        # Optimal tip: Update directly to the current module so that next time you don't have to go through __getattr__ again
        globals()[name] = attr
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
        
__all__ = [
        'make_blog_category',               # type: ignore
        'make_blog_tag',                    # type: ignore
        'make_blog_post',                   # type: ignore
        'make_blog_section',                # type: ignore
        'make_car_description',             # type: ignore
        'make_car_description_section',     # type: ignore
        'make_brand_history',               # type: ignore
        'make_brand_history_section',       # type: ignore
    ] 