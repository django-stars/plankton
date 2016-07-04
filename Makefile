test:
	python plankton/plankton_server.py & echo $$! > plankton_test_server.PID
	sleep 3
	python -m tests.test_server || echo "Failed"
	kill `cat plankton_test_server.PID`
	rm plankton_test_server.PID
