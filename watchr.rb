def run_test(testfile)
  puts "\npython #{testfile}"
  system("nosetests #{testfile}")
end

watch('gml_analyzer/([^\/]+)\.py') do |f|
  run_test("gml_analyzer/test/test_#{f[1]}.py")
end

watch('gml_analyzer/test/.*\.py') do |f|
  run_test(f)
end