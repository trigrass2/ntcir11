require 'systemu'

WORKSPACE_PATH = './workspace'
WORKSPACE_RESULT_PATH = './workspace/result'
WORKSPACE_TMP_PATH = './workspace/tmp'
FORMAT_RESULT_PATH = './NTCIR11/evaluation/result.txt'
MAP_JAR_PATH = './NTCIR11/evaluation/evalsqscr.jar'

def systemu_msg sh
  status, stdout, stderr = systemu sh
  res = {
      out: stdout,
      error: stderr,
      msg: [ '$Run shell: '+sh, '$Error: '+stderr ].join("\n")+"\n"
  }
end

# project パラメータを指定していないと弾く
def project_param_abort
  if !ENV['p'] 
      abort "paramater not found :: rake p=project_name task"
  end
end

#//////////////
# workflow
#//////////////

# 1. projectを作成
# 2. main.pyに結果を格納するコードを作成
# 3. rake p=tfidf all

#///////////////
# task
#///////////////

task :all => [:clean, :main, :format, :map]
# 計算結果をキャッシュしたソースを消さない
task :all_soft => [:clean_result, :clean_format, :main, :format, :map]
task :clean => [:clean_result, :clean_format, :clean_tmp]

task :init do
  Dir.glob(WORKSPACE_PATH+'/*') do |path|
    FileUtils.mkdir(path+'/tmp') if !FileTest.exist?(path+'/tmp')
    FileUtils.mkdir(path+'/result') if !FileTest.exist?(path+'/result')
  end
end

task :main do |t|
  # 実行
  project_param_abort()
  exe = "python #{WORKSPACE_PATH}/#{ENV['p']}/main.py"
  puts systemu_msg(exe)[:msg]
end

task :format do |t|
  # 中間ファイル作成
  project_param_abort()
  if Dir.glob(WORKSPACE_PATH+"/"+ENV['p']+'/result/*').size == 0
    puts "ERROR: workspace results is not exist"
    exit
  end
  project_path = File.expand_path("../#{WORKSPACE_PATH}/#{ENV['p']}/result", __FILE__) 
  format = "ruby ./NTCIR11/evaluation/formatter.rb #{project_path}"
  puts systemu_msg(format)[:msg]
end

task :map do
  # 結果の表示
  if !FileTest.exist?(FORMAT_RESULT_PATH)
    puts "ERROR: format result file is not found"
    exit
  end
  Dir.chdir("./NTCIR11/evaluation/") do
    map = "java -jar ./evalsqscr.jar ./result.txt"
    puts systemu_msg(map)[:msg]
    puts systemu_msg(map)[:out]
  end
end

task :clean_result do |t|
  # main.pyの実行結果を削除
  project_param_abort()
  FileUtils.rm(Dir.glob(WORKSPACE_PATH+"/"+ENV['p']+'/result/*'))
end

task :clean_format do 
  if FileTest.exist?(FORMAT_RESULT_PATH)
    FileUtils.rm(FORMAT_RESULT_PATH) 
  end
end

task :clean_tmp do |t|
  # tmpファイルを削除
  project_param_abort()
  FileUtils.rm(Dir.glob(WORKSPACE_PATH+"/"+ENV['p']+'/tmp/*'))
end
