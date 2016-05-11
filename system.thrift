namespace java system
namespace py system

enum statusCode
{
	PROCESSING = 0, //dang chay mo phong
	FINISHED = 1, 	//mo phong hoan thanh
	ERROR = 2 		//xay ra loi: sai session ID
}

struct SessionStatus
{
	1: statusCode status,
	2: string sessionID
}

struct Result 
{
	1: statusCode status,
	2: string benchmark_result,
	3: optional binary tracefile 
}

service SimulationSystemService 
{
	SessionStatus simulate(1:binary sessionFile)
	SessionStatus getSessionStatus(1:string sessionID)
	Result getResultFile(1:string sessionID)
}

