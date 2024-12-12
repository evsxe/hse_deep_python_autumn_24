#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

PyObject* parse_json_string(const char* json_str);

PyObject* custom_json_loads(PyObject* self, PyObject* args) {
    const char* json_str;

    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Expected a JSON string");
        return NULL;
    }

    return parse_json_string(json_str);
}


PyObject* parse_json_string(const char* json_str) {
    if (*json_str != '{') {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON: missing opening brace");
        return NULL;
    }

    PyObject* dict = PyDict_New();
    if (!dict) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create dictionary");
        return NULL;
    }

    json_str++; // Skip '{'

    while (*json_str != '\0' && *json_str != '}') {
        while (*json_str == ' ') json_str++; // Skip whitespace

        if (*json_str != '"') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON: expected key");
            Py_DECREF(dict);
            return NULL;
        }

        json_str++; // Skip '"'

        const char* key_start = json_str;
        size_t key_len = 0;
        while (*json_str != '\0' && *json_str != '"') {
            json_str++;
            key_len++;
        }

        if (*json_str != '"') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON: unterminated key");
            Py_DECREF(dict);
            return NULL;
        }

        PyObject* key = PyUnicode_FromStringAndSize(key_start, key_len);
        if (!key) {
            PyErr_SetString(PyExc_ValueError, "Failed to create key");
            Py_DECREF(dict);
            return NULL;
        }

        json_str++; // Skip '"'

        while (*json_str == ' ') json_str++; // Skip whitespace

        if (*json_str != ':') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON: missing colon");
            Py_DECREF(key);
            Py_DECREF(dict);
            return NULL;
        }

        json_str++; // Skip ':'

        while (*json_str == ' ') json_str++; // Skip whitespace

        PyObject* value = NULL;
        if (*json_str == '"') {
            json_str++; // Skip '"'
            const char* value_start = json_str;
            size_t value_len = 0;
            while (*json_str != '\0' && *json_str != '"') {
                json_str++;
                value_len++;
            }
            if (*json_str != '"') {
                PyErr_SetString(PyExc_ValueError, "Invalid JSON: unterminated string value");
                Py_DECREF(key);
                Py_DECREF(dict);
                return NULL;
            }
            value = PyUnicode_FromStringAndSize(value_start, value_len);
            json_str++; // Skip '"'
        } else if ((*json_str >= '0' && *json_str <= '9') || *json_str == '-') {
            long num = strtol(json_str, (char**)&json_str, 10);
            value = PyLong_FromLong(num);
        } else {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON: unexpected value type");
            Py_DECREF(key);
            Py_DECREF(dict);
            return NULL;
        }

        if (!value || PyDict_SetItem(dict, key, value) < 0) {
            PyErr_SetString(PyExc_ValueError, "Failed to set dictionary item");
            Py_DECREF(key);
            Py_DECREF(value);
            Py_DECREF(dict);
            return NULL;
        }

        Py_DECREF(key);
        Py_DECREF(value);

        while (*json_str == ' ') json_str++; // Skip whitespace

        if (*json_str == '}') break;
        if (*json_str != ',') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON: missing comma");
            Py_DECREF(dict);
            return NULL;
        }
        json_str++; // Skip ','
    }

    if (*json_str != '}') {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON: missing closing brace");
        Py_DECREF(dict);
        return NULL;
    }

    return dict;
}


static PyObject* custom_json_dumps(PyObject* self, PyObject* args) {
    PyObject* obj;
    if (!PyArg_ParseTuple(args, "O", &obj) || !PyDict_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return NULL;
    }

    PyObject* items = PyDict_Items(obj);
    if (!items) {
        PyErr_SetString(PyExc_MemoryError, "Failed to get dictionary items");
        return NULL;
    }

    Py_ssize_t num_items = PyList_GET_SIZE(items);
    size_t size = 2; //For {}

    for (Py_ssize_t i = 0; i < num_items; i++) {
        PyObject* item = PyList_GetItem(items, i);
        PyObject* key = PyTuple_GetItem(item, 0);
        PyObject* value = PyTuple_GetItem(item, 1);

        if (!PyUnicode_Check(key)) {
            PyErr_SetString(PyExc_TypeError, "Key must be a string");
            Py_DECREF(items);
            return NULL;
        }
        const char* key_str = PyUnicode_AsUTF8(key);
        size += strlen(key_str) + 3; //"key":


        if (PyLong_Check(value)) {
            char buf[25];
            snprintf(buf, sizeof(buf), "%ld", PyLong_AsLong(value));
            size += strlen(buf);
        } else if (PyUnicode_Check(value)) {
            const char* value_str = PyUnicode_AsUTF8(value);
            size += strlen(value_str) + 2; //""
        } else {
            PyErr_SetString(PyExc_TypeError, "Value must be a number or string");
            Py_DECREF(items);
            return NULL;
        }
        if (i < num_items -1) size++; //for ,
    }


    char* json_str = (char*)malloc(size);
    if (!json_str) {
        PyErr_SetString(PyExc_MemoryError, "Memory allocation failed");
        Py_DECREF(items);
        return NULL;
    }
    json_str[0] = '{';
    json_str[1] = '\0';
    size_t len = 1;


    for (Py_ssize_t i = 0; i < num_items; i++) {
        PyObject* item = PyList_GetItem(items, i);
        PyObject* key = PyTuple_GetItem(item, 0);
        PyObject* value = PyTuple_GetItem(item, 1);
        const char* key_str = PyUnicode_AsUTF8(key);
        size_t key_len = strlen(key_str);

        snprintf(json_str + len, size - len, "\"%.*s\":", (int)key_len, key_str);
        len += key_len + 3;

        if (PyLong_Check(value)) {
            char buf[25];
            snprintf(buf, sizeof(buf), "%ld", PyLong_AsLong(value));
            strcat(json_str + len, buf);
            len += strlen(buf);
        } else {
            const char* value_str = PyUnicode_AsUTF8(value);
            size_t value_len = strlen(value_str);
            snprintf(json_str + len, size - len, "\"%.*s\"", (int)value_len, value_str);
            len += value_len + 2;
        }

        if (i < num_items - 1) {
            strcat(json_str + len, ",");
            len++;
        }
    }
    strcat(json_str + len, "}");

    Py_DECREF(items);
    PyObject* result = Py_BuildValue("s", json_str);
    free(json_str);
    return result;
}

static PyMethodDef custom_json_methods[] = {
    {"loads", custom_json_loads, METH_VARARGS, "Deserialize JSON string to dictionary"},
    {"dumps", custom_json_dumps, METH_VARARGS, "Serialize dictionary to JSON string"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef custom_json_module = {
    PyModuleDef_HEAD_INIT,
    "custom_json",
    NULL,
    -1,
    custom_json_methods
};

PyMODINIT_FUNC PyInit_custom_json(void) {
    return PyModule_Create(&custom_json_module);
}
