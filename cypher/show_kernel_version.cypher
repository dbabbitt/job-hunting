
CALL dbms.components() YIELD name, versions, edition UNWIND versions as version RETURN name, version, edition;