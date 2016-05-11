namespace java graphicaleditor.connection
namespace py system

enum StatusCode
{
	PROCESSING = 0,
	FINISHED = 1,
	ERROR = 2
}

struct SessionStatus
{
	1: StatusCode status,
	2: string sessionID
}

struct Result 
{
	1: StatusCode status,
	2: string benchmark_result,
	3: optional binary tracefile 
}

service SimulationSystemService 
{
	string ping()
	SessionStatus simulate(1:binary sessionFile)
	SessionStatus getSessionStatus(1:string sessionID)
	Result getResultFile(1:string sessionID)
}

