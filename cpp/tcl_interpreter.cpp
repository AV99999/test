#include <tcl.h>
#include "db.h"
#include "dbDatabase.h"
#include "dbLib.h"
#include "dbTech.h"
#include "defin.h"
#include "lefin.h"

using namespace odb;

static dbDatabase* db = nullptr;

int read_lef_cmd(ClientData, Tcl_Interp* interp, int objc, Tcl_Obj* const objv[]) {
    if (objc < 2) {
        Tcl_WrongNumArgs(interp, 1, objv, "filename1 [filename2 ...]");
        return TCL_ERROR;
    }

    if (!db) {
        db = dbDatabase::create();
        if (!db) {
            Tcl_SetResult(interp, (char *)"Failed to create OpenDB database", TCL_STATIC);
            return TCL_ERROR;
        }
    }

    lefin reader(db, db->getTech());

    for (int i = 1; i < objc; i++) {
        const char* lef_file = Tcl_GetString(objv[i]);

        // generate unique lib name per LEF
        std::string lib_name = std::string("lib") + std::to_string(i);

        if (!reader.createTechAndLib(lib_name.c_str(), lef_file)) {
            Tcl_SetResult(interp, (char *)"Failed to read LEF file", TCL_STATIC);
            return TCL_ERROR;
        }
    }

    Tcl_SetResult(interp, (char *)"LEF read successfully", TCL_STATIC);
    return TCL_OK;
}

int read_def_cmd(ClientData, Tcl_Interp* interp, int objc, Tcl_Obj* const objv[]) {
    if (objc != 2) {
        Tcl_WrongNumArgs(interp, 1, objv, "filename");
        return TCL_ERROR;
    }

    const char* def_file = Tcl_GetString(objv[1]);

    if (!db) {
        db = dbDatabase::create();
        if (!db) {
            Tcl_SetResult(interp, (char *)"Failed to create OpenDB database", TCL_STATIC);
            return TCL_ERROR;
        }
    }

    dbLib* lib = db->getLibs().empty() ? nullptr : *db->getLibs().begin();
    if (!lib) {
        Tcl_SetResult(interp, (char *)"No LEF loaded. Load LEF before DEF.", TCL_STATIC);
        return TCL_ERROR;
    }

    std::vector<dbLib*> search_libs = { lib };
    defin reader(db);
    reader.createChip(search_libs, def_file);

    Tcl_SetResult(interp, (char *)"DEF read successfully", TCL_STATIC);
    return TCL_OK;
}

extern "C" int Tclapp_Init(Tcl_Interp *interp) {
    if (Tcl_Init(interp) == TCL_ERROR)
        return TCL_ERROR;

    Tcl_CreateObjCommand(interp, "read_lef", read_lef_cmd, nullptr, nullptr);
    Tcl_CreateObjCommand(interp, "read_def", read_def_cmd, nullptr, nullptr);
    return TCL_OK;
}

