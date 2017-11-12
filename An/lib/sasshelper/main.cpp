#define ADD_EXPORTS

#include <stdlib.h>
#include <string.h>
#include <sass/context.h>
#include <sass/base.h>

extern "C" {
	void ADDAPI set_include_path(const char *text);
	int  ADDAPI sass_compile_string(const char *text, char *include_path = NULL);
	int  ADDAPI sass_compile_file(const char *text);
	void ADDAPI sass_get_result(char *buff);
}

#ifdef _WIN32
#define SASS_FUNC(fn)      decltype(sass_##fn)* my_##fn;
#define _STR(x) #x
#define SASS_FUNC_INIT(fn) my_##fn = (decltype(my_##fn)) GetProcAddress(hDllInst, _STR(sass_##fn));
#define MY_(fn) my_##fn

// common
SASS_FUNC(option_set_precision)
SASS_FUNC(option_set_source_comments)
SASS_FUNC(option_push_include_path)
SASS_FUNC(context_get_output_string)
SASS_FUNC(context_get_error_status)
SASS_FUNC(context_get_error_message)
SASS_FUNC(context_get_options)

// data
SASS_FUNC(make_data_context)
SASS_FUNC(data_context_get_context)
SASS_FUNC(compile_data_context)
SASS_FUNC(delete_data_context)

// file
SASS_FUNC(make_file_context)
SASS_FUNC(file_context_get_context)
SASS_FUNC(compile_file_context)
SASS_FUNC(delete_file_context)


HINSTANCE hDllInst   = nullptr;

#else

#define MY_(fn) sass_##fn

#endif // _WIN32

struct Result {
	enum { STRING, FILE } type;
	union 
	{
		Sass_Data_Context* data_ctx;
		Sass_File_Context* file_ctx;
	};
	Sass_Context* ctx;
	const char* result_text;

	int put_result(int);
	void release();
} g_result;

char *g_include_path = nullptr;

/**
 * 存储全局字符串
 */
void put_global_string(char* &string, const char* text)
{
	void *tmp = realloc(string, strlen(text) + 1);
	if (tmp)
	{
		string = (char *)tmp;
		strcpy(string, text);
	}
}

/**
* 设置包含路径
*/
void set_include_path(const char *include_path)
{
	put_global_string(g_include_path, include_path);
}

void set_options(Sass_Options *options) {
	MY_(option_set_precision)(options, 10);
	if (g_include_path)
		MY_(option_push_include_path)(options, g_include_path);
}

int sass_compile_string(const char *text, char *include_path)
{
	char *source = (char *)malloc(strlen(text) + 1);
	strcpy(source, text);
	// note: sass 会自动free source
	g_result.data_ctx = MY_(make_data_context)(source);
	g_result.ctx = MY_(data_context_get_context)(g_result.data_ctx);
	g_result.type = g_result.STRING;
	Sass_Options *options = MY_(context_get_options)(g_result.ctx);
	set_options(options);
	if (include_path)
		MY_(option_push_include_path)(options, include_path);

	int status = MY_(compile_data_context)(g_result.data_ctx);
	return g_result.put_result(status);
}

int sass_compile_file(const char * input)
{
	// create the file context and get all related structs
	g_result.file_ctx = MY_(make_file_context)(input);
	g_result.ctx = MY_(file_context_get_context)(g_result.file_ctx);
	Sass_Options* options = MY_(context_get_options)(g_result.ctx);

	set_options(options);

	int status = MY_(compile_file_context)(g_result.file_ctx);
	return g_result.put_result(status);
}

void sass_get_result(char * buff)
{
	strcpy(buff, g_result.result_text);
	g_result.release();
}


int Result::put_result(int status)
{
	if (status == 0)
		result_text = MY_(context_get_output_string)(g_result.ctx);
	else
		result_text = MY_(context_get_error_message)(g_result.ctx);

	int size = strlen(result_text) + 1;
	return (size << 1) | ((status == 0) & 1);
}

void Result::release()
{
	// release allocated memory
	if (type == STRING)
	{
		MY_(delete_data_context)(data_ctx);
	}
	else if (type == FILE) {
		MY_(delete_file_context)(file_ctx);
	}
	data_ctx = nullptr;
	ctx = nullptr;
	result_text = nullptr;
}


#ifdef _WIN32

#include <windows.h>

void loadLibSass(HANDLE hModule)
{
	TCHAR buff[128];
	auto length = GetModuleFileName((HMODULE)hModule, buff, sizeof(buff));
	// 最后一个分隔符的位置
	LPTSTR ptr = wcsrchr(buff, L'\\');
	if (ptr)
		*ptr = NULL;
	SetDllDirectory(buff);


	hDllInst = LoadLibrary(L"libsass.dll");
	if (hDllInst)
	{
		// common
		SASS_FUNC_INIT(option_set_precision)
		SASS_FUNC_INIT(option_set_source_comments)
		SASS_FUNC_INIT(option_push_include_path)
		SASS_FUNC_INIT(context_get_output_string)
		SASS_FUNC_INIT(context_get_error_status)
		SASS_FUNC_INIT(context_get_error_message)
		SASS_FUNC_INIT(context_get_options)

		// data
		SASS_FUNC_INIT(make_data_context)
		SASS_FUNC_INIT(data_context_get_context)
		SASS_FUNC_INIT(compile_data_context)
		SASS_FUNC_INIT(delete_data_context)

		// file
		SASS_FUNC_INIT(make_file_context)
		SASS_FUNC_INIT(file_context_get_context)
		SASS_FUNC_INIT(compile_file_context)
		SASS_FUNC_INIT(delete_file_context)
	}
}

#ifdef ADD_EXPORTS

BOOL APIENTRY DllMain(HANDLE hModule,
	DWORD  ul_reason_for_call,
	LPVOID lpReserved
)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		loadLibSass(hModule);
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
		break;
	case DLL_PROCESS_DETACH:
		if (hDllInst)
		{
			FreeLibrary(hDllInst);
		}
		break;
	}
	return TRUE;
}

#else

#include "stdio.h"

int main()
{
	loadLibSass(NULL);

	int data = sass_compile_string("$fontSize: 12px;\nbody{\n    font-size:$fontSize;\n}");
	if (data & 1)
	{
		int size = data >> 1;
		printf("size: %d\n", size);
		char *buff = (char *)malloc(size);
		sass_get_result(buff);
		printf(buff);
		free(buff);
	}

	FreeLibrary(hDllInst);
}
#endif // ADD_EXPORTS

#else

#ifndef ADD_EXPORTS

#include "stdio.h"

int main()
{
	int data = sass_compile_string(".layout {\n	padding: 5px;\n	overflow: hidden;\n\n	.btns {\n		padding: 10px 0;\n		button {\n			font-family: 'icon';\n		}	\n	}\n}\n\n.raw, #html {\n	float: left;\n	width: 50%;\n	height: 600px;\n	box-sizing: border-box;\n}\n\n.raw {\n	#inputer {\n		box-sizing: border-box;\n		height: 100%;\n		width: 100%;\n		vertical-align: top;\n		padding: 10px;\n		resize: none;\n		border: none;\n		background-color: #f5f5f5;\n		outline: none;\n		font-family: inherit;\n		color: #616161;\n		box-shadow: 0 0 3px #aaa;\n		transition: all ease .3s;\n	}\n}\n\n#html {\n	padding: 10px;\n	box-shadow: 0 0 3px #aaa;\n	overflow: auto;\n}");
	if (data & 1)
	{
		int size = data >> 1;
		printf("size: %d\n", size);
		char *buff = (char *)malloc(size);
		sass_get_result(buff);
		printf(buff);
		free(buff);
	}
}
#endif // ADD_EXPORTS

#endif // _WIN32