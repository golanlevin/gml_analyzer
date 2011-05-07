def run_test(testfile)
  puts "\npython #{testfile}"
  system("nosetests #{testfile}")
end

def run_all_tests
  system("nosetests")
end

watch('gml_analyzer/([^\/]+)\.py') do |f|
  # run_test("gml_analyzer/test/test_#{f[1]}.py")
  run_all_tests
end

watch('gml_analyzer/test/.*\.py') do |f|
  run_test(f)
end