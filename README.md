<link rel="stylesheet" href="https://static.tiangong.cn/fe/skywork-site-assets/styles/doc_reference_style.css?v=1944412015364517888"/></head>
<body><div class="container">
<h1 id="section-1">梯网化焊接修复参数优化系统 (Ladder-Networked Welding Repair Parameter Optimization System)</h1>
<div class="toc">
<h2 id="section-1">📓 目录</h2>
<ul>
<li><a href="#-项目简介-about-the-project">项目简介 (About The Project)</a></li>
<li><a href="#-核心功能-features">核心功能 (Features)</a>
<ul>
<li><a href="#-智能参数优化与ai建议">🤖 智能参数优化与AI建议</a></li>
<li><a href="#-多维数据可视化">📊 多维数据可视化</a></li>
<li><a href="#-三维模型路径切片与仿真">🌐 三维模型路径切片与仿真</a></li>
<li><a href="#-梯网化结构设计与增材控形">🏗️ 梯网化结构设计与增材控形</a></li>
</ul>
</li>
<li><a href="#-技术栈-tech-stack">技术栈 (Tech Stack)</a></li>
<li><a href="#-安装与运行-getting-started">安装与运行 (Getting Started)</a>
<ul>
<li><a href="#-环境要求-prerequisites">1. 环境要求 (Prerequisites)</a></li>
<li><a href="#-安装步骤-steps">2. 安装步骤 (Steps)</a></li>
<li><a href="#-运行项目">3. 运行项目</a></li>
</ul>
</li>
<li><a href="#-快速上手指南-quick-start">快速上手指南 (Quick Start)</a></li>
<li><a href="#-模块详解-module-breakdown">模块详解 (Module Breakdown)</a></li>
<li><a href="#-贡献指南-contributing">贡献指南 (Contributing)</a></li>
<li><a href="#-许可证-license">许可证 (License)</a></li>
</ul>
</div>
<p>
</p>
<blockquote>
            一个集智能路径规划、AI参数优化、多维数据可视化与实时仿真于一体的先进焊接修复工业软件平台。
        </blockquote>
<h2 id="section--项目简介-about-the-project">📖 项目简介 (About The Project)</h2>
<p>
            焊接作为现代工业的基石，其应用无处不在。然而，当焦点从标准化的大规模生产转向高价值、非标件的修复时，挑战呈指数级增长。焊接修复，特别是针对大型锻造模具、航空发动机叶片或关键承重构件的修复，远非简单的“填补缺陷”。它是一个涉及材料科学、热力学、机器人学和过程控制的复杂系统工程。
        </p>
<p>
            传统的修复流程高度依赖资深技师的“手感”和经验，这种模式面临着诸多瓶颈：
        </p>
<ul>
<li><strong>参数设定的盲目性</strong>：焊接参数（如电压、电流、送丝速度、焊接速度等）的组合空间巨大，寻找最优解如同大海捞针。不当的参数会导致裂纹、气孔、未熔合等致命缺陷，造成不可逆的损失。<a href="https://www.lowcostwelder.com/profispot-pressure-welding-controllers/spot-welding-parameters-parameters-in-resistance-or-pressure-welding" target="_blank">参数设定的复杂性被认为是焊接工艺中的核心痛点之一</a>。<em data-skywork="text_badge" data-sk-source-text="参数设定的盲目性：焊接参数（如电压、电流、送丝速度、焊接速度等）的组合空间巨大，寻找最优解如同大海捞针。不当的参数会导致裂纹、气孔、未熔合等致命缺陷，造成不可逆的损失。参数设定的复杂性被认为是焊接工艺中的核心痛点之一。" id="skTag-P6UEQV" class="sk-source-tag" data-sk-source-id="P6UEQV"></em></li>
<li><strong>路径规划的低效性</strong>：修复区域的几何形状往往不规则，手动编程或简单的CAD/CAM路径无法保证恒定的焊接姿态和速度，影响修复层质量的均匀性。</li>
<li><strong>过程的“黑箱”状态</strong>：焊接过程瞬息万变，缺乏实时监控和质量预测手段，使得问题只能在焊后检测中发现，错失了过程控制的最佳时机。</li>
<li><strong>知识传承的断层</strong>：宝贵的修复经验固化在少数专家的头脑中，难以被系统化地记录、传承和复用，制约了行业整体水平的提升。</li>
</ul>
<p>
            本项目 <strong>“梯网化焊接修复参数优化系统”</strong> 正是为应对上述挑战而设计。它不仅仅是一个软件工具，更是一个集成了先进制造理念与人工智能技术的综合性解决方案。系统引入了“梯网化”复合结构和“增材控形”等前沿概念，旨在通过分层、异质的材料填充策略，提升修复区域的抗疲劳和抗开裂性能。
        </p>
<p>
            通过深度融合三维模型处理、AI大模型驱动的参数优化、多物理场数据可视化以及机器人运动学仿真，本系统构建了一个从“诊断”（模型导入与分析）到“开方”（AI参数推荐）、再到“治疗”（路径规划与仿真）的闭环工作流。我们的目标是：将焊接修复从一门“艺术”转变为一门精确、可控、可预测的“科学”，赋能工程师，降低对个人经验的依赖，最终实现更高质量、更高效率、更低成本的绿色再制造。
        </p>
<figure>
<img alt="自动化焊接机器人" src="https://picture-search.tiangong.cn/image/rt/0f999caf1b94aea408cfbcae66777a63.jpg" style="max-height: 280px; max-width: 100%;"/>
<figcaption>系统旨在赋能自动化焊接机器人，实现对复杂工件的精准修复</figcaption>
</figure>
<h2 id="section--核心功能-features">🚀 核心功能 (Features)</h2>
<p>
            本系统通过模块化的设计，集成了四大核心功能板块，为用户提供从模型到修复的全链路支持。
        </p>
<h3 id="section--智能参数优化与ai建议">🤖 智能参数优化与AI建议</h3>
<p>
            参数优化是焊接修复的灵魂。本系统将传统的手动试错过程，升级为数据驱动和AI辅助的智能决策过程。
        </p>
<ul>
<li><strong>多参数联动调节</strong>: 用户界面提供了滑块、旋钮、输入框等多种交互方式，允许工程师直观、精确地调节电压、电流、送丝速度、焊接速度、材料厚度等核心工艺参数。所有控件双向绑定，修改任一控件，其他相关控件会同步更新，确保了操作的一致性。</li>
<li><strong>一键AI优化</strong>: 这是系统的“大脑”。通过集成阿里云通义千问（Dashscope）大模型，系统能够理解当前的工艺参数组合和修复目标。用户只需点击“参数优化”按钮，系统便会将当前工况打包成结构化提示（Prompt），发送至云端AI。AI模型会根据其庞大的知识库，返回针对性的优化建议。这些建议不仅包括具体的参数调整方向（例如，“建议将电压提高5%，同时降低焊接速度10%”），还涵盖了预期的质量提升和潜在风险提示（例如，“可能增加热输入，注意控制变形”）。<a href="https://www.linkedin.com/pulse/ai-welding-parameter-optimization-ruthuraraj-r-d330c" target="_blank">正如行业分析所指出的，AI能够通过分析传感器数据和历史记录，预测参数变化对焊接质量的影响，从而避免缺陷</a>。<em data-skywork="text_badge" data-sk-source-text="一键AI优化: 这是系统的“大脑”。通过集成阿里云通义千问（Dashscope）大模型，系统能够理解当前的工艺参数组合和修复目标。用户只需点击“参数优化”按钮，系统便会将当前工况打包成结构化提示（Prompt），发送至云端AI。AI模型会根据其庞大的知识库，返回针对性的优化建议。这些建议不仅包括具体的参数调整方向（例如，“建议将电压提高5%，同时降低焊接速度10%”），还涵盖了预期的质量提升和潜在风险提示（例如，“可能增加热输入，注意控制变形”）。正如行业分析所指出的，AI能够通过分析传感器数据和历史记录，预测参数变化对焊接质量的影响，从而避免缺陷。" id="skTag-P6UERR" class="sk-source-tag" data-sk-source-id="P6UERR"></em></li>
<li><strong>多语言支持</strong>: 考虑到全球化协作的需求，AI建议模块支持中文、英语、日语、西班牙语等多种语言，一键切换，无缝对接国际团队。</li>
<li><strong>知识库驱动</strong>: 每一次成功的优化案例（即用户采纳并验证有效的参数组合）都会被自动记录到本地的知识库中。这个知识库不仅是宝贵的数字资产，更是未来AI模型进行微调（Fine-tuning）和提供更精准推荐的数据基础，形成了一个持续学习和进化的闭环。</li>
</ul>
<h3 id="section--多维数据可视化">📊 多维数据可视化</h3>
<p>
            如果说AI是决策的大脑，那么数据可视化就是洞察过程的眼睛。本系统将抽象的焊接数据转化为直观的图形，帮助工程师洞悉瞬息万变的焊接过程。
        </p>
<ul>
<li><strong>实时质量监控</strong>: 主界面的“质量仪表盘”和“质量趋势图”是操作员的核心看板。仪表盘以指针形式实时显示当前模拟的焊接质量评分，并通过红、橙、绿三个颜色区域（分别对应不合格、良好、优秀）提供直观的质量等级判断。趋势折线图则记录了质量评分随时间的变化轨迹，帮助识别工艺的稳定性。这种实时反馈机制，使得工程师能够即时调整参数，防止缺陷的产生。<a href="https://aws.amazon.com/blogs/industries/artificial-intelligence-in-industrial-welding-produces-near-real-time-insights-through-virtually-100-sample-sizes/" target="_blank">近乎实时的洞察是提升焊接质量和效率的关键</a>。<em data-skywork="text_badge" data-sk-source-text="实时质量监控: 主界面的“质量仪表盘”和“质量趋势图”是操作员的核心看板。仪表盘以指针形式实时显示当前模拟的焊接质量评分，并通过红、橙、绿三个颜色区域（分别对应不合格、良好、优秀）提供直观的质量等级判断。趋势折线图则记录了质量评分随时间的变化轨迹，帮助识别工艺的稳定性。这种实时反馈机制，使得工程师能够即时调整参数，防止缺陷的产生。近乎实时的洞察是提升焊接质量和效率的关键。" id="skTag-B6ONQ1" class="sk-source-tag" data-sk-source-id="B6ONQ1"></em></li>
<li><strong>参数-质量三维热力图</strong>: 为了揭示多个参数之间的非线性耦合关系，系统采用 `pyqtgraph.opengl` 绘制了“电压-送丝速度-质量”三维热力图。在这个三维空间中，工程师可以清晰地看到高质量区域（绿色峰顶）和缺陷区域（红色谷底）的分布，从而快速定位出最佳的工艺窗口。这比传统的二维曲线图提供了更丰富的维度和更深刻的洞察。</li>
<li><strong>优化效果对比</strong>: 任何优化措施的效果都需要量化评估。系统通过简洁的柱状图，直观对比“优化前”与“优化后”的质量评分，使优化带来的价值提升一目了然。</li>
<li><strong>多源数据融合看板</strong>: 现代焊接机器人是多种传感器的集合体。本系统模拟采集了ABB机械臂的多源数据流，包括电流、电压、TCP（工具中心点）坐标、六轴关节角、运行速度、焊枪温度，乃至模拟的视觉（缺陷概率）和声学（噪声分贝）信号。这些数据在“多源监测”Tab页中以表格和实时曲线的形式统一展示，为高级工程师进行深度调试和故障诊断提供了全面的数据支持。</li>
</ul>
<div class="chart-container" id="canvas-parent-1">
<canvas id="qualityTrendChart"></canvas>
</div>
<figcaption>图3：模拟的焊接质量实时趋势图，展示了质量评分随时间的变化及预警区间</figcaption>
<div class="chart-container" id="canvas-parent-2">
<canvas id="optimizationCompareChart"></canvas>
</div>
<figcaption>图4：参数优化前后效果对比柱状图，直观量化AI建议带来的质量提升</figcaption>
<h3 id="section--三维模型路径切片与仿真">🌐 三维模型路径切片与仿真</h3>
<p>
            精确的修复路径是保证修复质量的前提。本系统提供了一套完整的从三维模型到机器人可执行代码的工作流。
        </p>
<ul>
<li><strong>通用模型支持</strong>: 系统能够直接导入行业标准的 `.stl`（三角网格）和 `.step`（实体/曲面）格式的三维模型文件。针对STEP文件，系统集成了强大的 `pythonocc-core` 库，能够解析复杂的B-rep几何实体，确保了对工业设计的广泛兼容性。</li>
<li><strong>高级切片算法</strong>: 内置的路径切片引擎基于 `trimesh` 和 `pythonocc-core`，提供了强大的切片能力。用户可以自定义层高、网格间距、优化等级等高级参数，以适应不同精度和效率的修复需求。算法能够自动处理复杂的几何形状，生成分层的修复轮廓。</li>
<li><strong>路径优化与平滑</strong>: 原始的切片路径往往存在大量的空走和不连续的急转弯。系统采用KD-Tree最近邻搜索等算法对路径点进行重排序，显著减少了非焊接运动时间，提高了整体效率。后续还可以集成路径平滑算法，确保机器人运动更加流畅，减少机械冲击。</li>
<li><strong>机器人轨迹仿真</strong>: 可视化是验证路径正确性的最有效手段。本系统利用 `PyVista` 这一高性能科学可视化库，在界面中嵌入了一个功能强大的3D渲染窗口。用户可以在导入模型后，实时观察生成的切片轮廓和优化后的焊接轨迹。更进一步，系统提供了轨迹仿真功能，以动画形式模拟ABB机器人的工具头沿路径运动的过程，并允许用户在仿真时对模型进行旋转、缩放、平移等交互操作，从任意角度检查路径的合理性。</li>
</ul>
<h3 id="section--梯网化结构设计与增材控形">🏗️ 梯网化结构设计与增材控形</h3>
<p>
            本系统不仅关注“如何焊”，更探索“焊什么结构”。通过引入先进的修复结构理念，为提升修复件的服役性能提供了新的思路。
        </p>
<ul>
<li><strong>梯网化结构可视化</strong>: “梯网化”是一种仿生复合结构理念，它模仿了生物组织中软硬材料的梯度分布。在焊接修复中，这意味着可以通过交替沉积不同性能的材料层（例如，硬质耐磨层和柔性过渡层），形成梯度功能材料，并在其中嵌入网格状的止裂结构。本系统通过一个专门的Tab页，将这一抽象概念可视化。用户可以通过滑块动态调整“止裂材料延展性”，并实时观察示意图中梯度层和网格结构的变化，从而直观理解不同设计对结构性能的潜在影响。</li>
<li><strong>增材控形路径规划</strong>: 焊接修复本质上是一种增材制造过程。修复层的填充路径直接决定了其内部的组织结构和应力分布。本系统在“增材控形”Tab页中，提供了多种典型的增材路径可视化，如螺旋、网格、直线、波浪等。这使得工程师能够在修复前就规划好填充策略，以达到控制残余应力、优化晶粒生长方向等目的，实现对修复层最终形状和性能的精确控制。</li>
</ul>
<h2 id="section--技术栈-tech-stack">🛠️ 技术栈 (Tech Stack)</h2>
<p>
            本项目是多种先进Python库协同工作的成果，构建了一个功能全面、性能可靠的工业级桌面应用。
        </p>
<table>
<thead>
<tr>
<th>类别</th>
<th>技术/库</th>
<th>在项目中的作用</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>GUI框架</strong></td>
<td><code>PyQt5</code></td>
<td>构建整个应用程序的图形用户界面，包括窗口、按钮、滑块、Tab页等所有交互元素。</td>
</tr>
<tr>
<td rowspan="2"><strong>2D数据可视化</strong></td>
<td><code>Matplotlib</code></td>
<td>用于生成静态的、高质量的2D图表，如趋势折线图、对比柱状图等。</td>
</tr>
<tr>
<td><code>pyqtgraph</code></td>
<td>一个专为科学和工程应用设计的高性能2D绘图库，用于实现质量仪表盘等需要高速刷新和交互的图表。</td>
</tr>
<tr>
<td rowspan="2"><strong>3D数据可视化/仿真</strong></td>
<td><code>PyVista</code></td>
<td>作为VTK（Visualization Toolkit）的高级封装，提供了强大且易用的3D科学可视化能力，用于显示STL/STEP模型、渲染焊接路径和实现机器人轨迹仿真。</td>
</tr>
<tr>
<td><code>pyqtgraph.opengl</code></td>
<td>用于实现高性能的3D实时数据可视化，如参数-质量关系的三维热力图。</td>
</tr>
<tr>
<td rowspan="3"><strong>3D模型处理</strong></td>
<td><code>trimesh</code></td>
<td>用于加载、处理和分析STL等三角网格模型，执行切片、布尔运算等核心几何操作。</td>
</tr>
<tr>
<td><code>pythonocc-core</code></td>
<td>OpenCASCADE技术的Python封装，提供了处理STEP等CAD实体模型的能力，是工业级几何处理的核心。</td>
</tr>
<tr>
<td><code>numpy</code></td>
<td>Python科学计算的基础库，为所有几何运算、数据处理和可视化提供了底层的数组和矩阵运算支持。</td>
</tr>
<tr>
<td><strong>AI大模型</strong></td>
<td><code>dashscope</code></td>
<td>阿里云官方SDK，用于与通义千问大模型进行API交互，获取智能参数优化建议。</td>
</tr>
<tr>
<td><strong>代码生成</strong></td>
<td><code>jinja2</code></td>
<td>一个现代且功能强大的模板引擎，用于根据路径点数据生成结构化的机器人控制代码（如ABB的RAPID代码）。</td>
</tr>
<tr>
<td><strong>其他</strong></td>
<td><code>pandas</code>, <code>scipy</code></td>
<td>Pandas用于数据管理和分析，Scipy则提供了更高级的科学计算功能，如插值、优化算法等，在数据处理和路径优化中发挥作用。</td>
</tr>
</tbody>
</table>
<h2 id="section--安装与运行-getting-started">📦 安装与运行 (Getting Started)</h2>
<p>
            请遵循以下步骤在您的本地环境中设置和运行本项目。由于项目依赖项较为复杂，强烈建议使用 `conda` 创建独立的虚拟环境。
        </p>
<h3 id="section--环境要求-prerequisites">1. 环境要求 (Prerequisites)</h3>
<ul>
<li><strong>Python</strong>: <code>3.8</code> 或更高版本。</li>
<li><strong>Conda</strong>: 推荐使用 <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">Miniconda</a> 或 Anaconda 来管理环境和依赖。</li>
<li><strong>C++ Build Tools</strong>: 在Windows上，安装 `pythonocc-core` 可能需要 <a href="https://visualstudio.microsoft.com/visual-cpp-build-tools/" target="_blank">Microsoft C++ Build Tools</a>。在Linux上，通常需要 `build-essential` 包。</li>
<li><strong>API Key</strong>: 一个有效的阿里云 <a href="https://help.aliyun.com/document_detail/2512515.html" target="_blank">Dashscope API Key</a>，用于驱动AI建议功能。</li>
</ul>
<h3 id="section--安装步骤-steps">2. 安装步骤 (Steps)</h3>
<ol>
<li>
<strong>克隆仓库</strong>
<pre><code>git clone https://github.com/your-username/your-repo.git
cd your-repo</code></pre>
</li>
<li>
<strong>创建并激活Conda环境 (推荐)</strong>
<pre><code>conda create -n welding_env python=3.8
conda activate welding_env</code></pre>
</li>
<li>
<strong>安装核心依赖</strong>
<p>由于 `pythonocc-core` 的特殊性，建议使用 `conda-forge` 渠道进行安装，这通常能解决大部分编译问题。</p>
<pre><code>conda install -c conda-forge pythonocc-core=7.6.0</code></pre>
</li>
<li>
<strong>安装其余依赖</strong>
<p>为了方便管理，建议将以下内容保存为 <code>requirements.txt</code> 文件，然后使用 `pip` 进行安装。</p>
<pre><code># requirements.txt
numpy
pandas
PyQt5
matplotlib
requests
pyqtgraph
jinja2
networkx
trimesh
scipy
dashscope
Pillow
pyvista</code></pre>
<p>然后运行安装命令：</p>
<pre><code>pip install -r requirements.txt</code></pre>
<p><strong>注意</strong>: 如果在安装 `pyvista` 时遇到问题，可以尝试 `pip install pyvista[all]` 来安装所有可选的后端。</p>
</li>
<li>
<strong>配置API Key</strong>
<p>在代码 `LLMWorker` 类中，找到以下行并替换为您的API Key：</p>
<pre><code># 在 LLMWorker.run 方法内
dashscope.api_key = &#34;sk-xxxxxxxxxxxxxxxxxxxxxxxx&#34;</code></pre>
<p>为了安全起见，更推荐的方式是使用环境变量。在您的操作系统中设置一个名为 `DASHSCOPE_API_KEY` 的环境变量，并在代码中使用 `os.getenv(&#34;DASHSCOPE_API_KEY&#34;)` 来读取。</p>
</li>
</ol>
<h3 id="section--运行项目">3. 运行项目</h3>
<p>
            确保您已激活 `conda` 环境，然后执行主程序脚本：
        </p>
<pre><code>python &#34;v3 - 副本.py&#34;</code></pre>
<p>
            程序启动后，会首先弹出一个启动选择对话框。您可以根据需要选择进入 **“主程序 - 焊接参数优化系统”** 或 **“路径切片与仿真系统”**。之后，会弹出登录界面，使用默认账号 <code>admin</code> 和密码 <code>123456</code> 即可登录。
        </p>
<h2 id="section--快速上手指南-quick-start">⚡ 快速上手指南 (Quick Start)</h2>
<p>
            以下是一个典型的端到端使用流程，旨在帮助您在5分钟内快速体验系统的核心价值。
        </p>
<ol>
<li>
<strong>启动与登录</strong>:
                <ul>
<li>运行程序 `python &#34;v3 - 副本.py&#34;`。</li>
<li>在弹出的启动选择对话框中，选择 **“主程序 - 焊接参数优化系统”**。</li>
<li>在登录界面，输入用户名 <code>admin</code> 和密码 <code>123456</code>，点击“登录”。</li>
</ul>
</li>
<li>
<strong>模型处理与路径规划</strong>:
                <ul>
<li>进入主界面后，系统默认显示 **“路径切片与仿真”** Tab页。</li>
<li>点击 **“导入模型”** 按钮，从文件浏览器中选择一个 `.stl` 或 `.step` 格式的三维模型文件。模型将显示在中央的3D视图中。</li>
<li>在右侧的参数面板中，您可以尝试调整 **层高(mm)** 或 **优化等级** 等参数。</li>
<li>点击 **“执行切片”** 按钮。稍等片刻，您会看到3D视图中叠加显示出红色的切片轮廓线。</li>
<li>接着，点击 **“路径优化”** 按钮。系统将对红色轮廓点进行排序和连接，生成一条蓝色的连续焊接轨迹。</li>
<li>最后，点击 **“轨迹仿真”** 按钮。一个红色的球点将沿着蓝色轨迹运动，模拟机器人的焊接过程。您可以用鼠标拖动3D视图，从不同角度观察仿真效果。</li>
</ul>
</li>
<li>
<strong>参数优化与实时监控</strong>:
                <ul>
<li>切换到 **“实时监控”** Tab页。</li>
<li>在界面左侧的 **“参数控制”** 面板，尝试拖动 **“电压 (V)”** 的滑块。观察右侧的 **“质量仪表盘”** 和 **“质量趋势”** 图表，它们的数值会（模拟地）随之变化。</li>
<li>点击橙色的 **“参数优化”** 按钮。</li>
<li>观察变化：左侧的滑块和旋钮会自动跳转到一组新的推荐值。同时，下方的 **“AI参数优化建议”** 窗口会刷新，显示出大模型生成的详细文字建议。右侧的 **“参数优化效果对比”** 图表也会更新，展示优化前后的质量评分差异。</li>
</ul>
</li>
<li>
<strong>深度分析与数据管理</strong>:
                <ul>
<li>切换到 **“参数分析”** Tab页。这里的3D热力图展示了不同参数组合下的质量分布情况，您可以拖动视图进行探索。</li>
<li>切换到 **“知识库”** Tab页。您会发现，刚才AI优化的那组参数已经被记录在了表格中。这个表格可以点击 **“导出知识库”** 按钮保存为 `.csv` 文件，用于后续的离线分析。</li>
</ul>
</li>
</ol>
<p>
            通过以上流程，您已经体验了从模型处理、路径规划、AI优化到数据分析和管理的完整闭环。
        </p>
<h2 id="section--模块详解-module-breakdown">🧩 模块详解 (Module Breakdown)</h2>
<p>
            系统UI采用多Tab页设计，将复杂的功能解耦到不同的工作区，每个模块都承载着特定的核心功能，共同构成一个有机的整体。
        </p>
<ul>
<li>
<strong>路径切片与仿真 (Path Slicing &amp; Simulation)</strong>:
                <p>这是所有修复工作的起点和几何基础。该模块的核心是 `ABBPathSlicerTab` 类，它深度集成了 `PyVista` 用于3D交互，`trimesh` 和 `pythonocc-core` 用于几何处理。其工作流是：
                </p><ol>
<li><strong>模型导入</strong>: 通过 `open_model` 方法，支持STL和STEP文件。STEP文件通过 `pythonocc-core` 的 `read_step_file` 读取，并利用 `BRepMesh_IncrementalMesh` 将其转换为三角网格，以便后续处理。这一步是兼容工业级CAD模型的关键。</li>
<li><strong>参数化切片</strong>: `run_slice` 方法是切片核心。它根据用户设定的层高，沿指定轴向（默认为Z轴）对三维网格进行平面切割，提取出一系列的二维轮廓（`section.discrete`）。</li>
<li><strong>路径优化</strong>: `run_optimize` 方法在一个独立的 `QThread` 中执行，以避免UI卡顿。它将所有轮廓点收集起来，利用 `scipy.spatial.KDTree` 构建一个快速近邻搜索结构，然后通过贪心算法（从一个点出发，不断寻找最近的未访问点）将离散的点云连接成一条连续的路径。</li>
<li><strong>轨迹仿真</strong>: `run_simulation` 方法使用 `QTimer` 创建动画循环。在每一步中，它都会更新 `PyVista` 视图，绘制出已走过的路径和当前工具头位置（一个红色小球），从而实现动态仿真。</li>
</ol>
<p></p>
</li>
<li>
<strong>实时监控 (Real-time Monitoring)</strong>:
                <p>这是系统的核心操作界面，强调人机交互和实时反馈。主要由左侧的控制面板和右侧的可视化面板组成。
                </p><ul>
<li><strong>控制面板</strong>: 包含多种参数输入控件，如 `QSlider`, `QComboBox`, 以及自定义的 `ParameterDial` 旋钮。这些控件的信号（如 `valueChanged`）被连接到更新函数，实现了参数的即时调整。</li>
<li><strong>可视化面板</strong>: 包含 `QualityMeter`（仪表盘）、`PredictionChart`（趋势图）等。这些图表通过定时器（`QTimer`）或事件回调（如参数调整后）进行刷新。例如，`update_prediction` 方法会模拟生成新的质量数据，并调用图表对象的 `update_plot` 或 `update_quality` 方法来更新显示。</li>
<li><strong>AI交互</strong>: “参数优化”按钮的点击事件会触发 `optimize_parameters` 方法。该方法会收集当前所有参数，构建一个符合预设模板的Prompt，然后创建一个 `LLMWorker` 线程来异步调用Dashscope API。当AI结果返回时，`LLMWorker` 会发出 `result_ready` 信号，主线程的 `handle_llm_response` 槽函数接收到信号后，将AI建议更新到UI上。</li>
</ul>
<p></p>
</li>
<li>
<strong>参数分析 (Parameter Analysis)</strong>:
                <p>此模块提供更深层次的数据洞察，帮助工程师理解工艺参数背后的物理规律。核心是 `HeatMap3D` 类，它使用 `pyqtgraph.opengl` 来绘制三维散点图和插值曲面。当用户切换到此Tab页时，`on_tab_changed` 会触发 `update_analysis_charts` 方法，该方法会生成一组模拟数据点（电压、速度、质量），并调用 `heatmap_3d.update_data`。在 `update_data` 内部，不仅会绘制出代表每个实验点的散点，当数据点足够多时，还会调用 `scipy.interpolate.griddata` 进行三维曲面插值，从而将离散的数据点拟合成一个光滑的质量响应曲面，工艺窗口一目了然。
                </p>
</li>
<li>
<strong>多源监测 (Multi-source Monitoring)</strong>:
                <p>该模块通过 `setup_multisource_data` 和 `update_multisource_data` 方法，使用一个 `QTimer` 定时模拟从ABB机器人控制器采集数据的过程。它维护一个字典 `multisource_data` 来存储各类传感器的最新值，并使用另一个字典 `data_history` 来记录历史数据。`update_multisource_data` 方法会随机生成模拟数据，并刷新界面上的 `QTableWidget` 和实时曲线图。此外，该模块还包含一个简单的报警逻辑，当模拟数据超过预设阈值时，会更新报警标签并记录报警历史。
                </p>
</li>
<li>
<strong>梯网化结构 &amp; 增材控形</strong>:
                <p>这两个模块是概念性的可视化展示。它们不涉及复杂的计算，而是通过 `Matplotlib` 绘制示意图。例如，`update_structure_plot` 方法会根据滑块的值（代表“延展性”）改变图中网格线的颜色，而 `update_forming_plot` 则根据下拉框选择的路径类型（螺旋、网格等）绘制出不同的几何路径。它们的作用是向用户传达先进的修复设计理念。
                </p>
</li>
<li>
<strong>知识库 (Knowledge Base)</strong>:
                <p>这是一个简单的数据持久化和管理模块。系统在内存中维护一个列表 `knowledge_base`，每次AI优化后，新的参数组合会作为一个字典追加到这个列表中。`append_log` 方法在记录日志的同时，会检查知识库是否有更新，并调用 `kb_table.setRowCount` 和 `kb_table.setItem` 来刷新UI表格。`export_knowledge_base` 方法则使用Python内置的 `csv` 模块，将这个列表写入到一个 `.csv` 文件中。
                </p>
</li>
<li>
<strong>操作日志 (Operation Log)</strong>:
                <p>最基础但重要的模块。`append_log` 方法是其核心，系统中的所有关键操作（如按钮点击、参数调整、AI调用等）都会调用此方法。它简单地将带有时间戳的日志信息追加到 `QTextEdit` 控件中，并自动滚动到底部，为问题追溯和操作复盘提供了依据。
                </p>
</li>
</ul>
<h2 id="section--贡献指南-contributing">🤝 贡献指南 (Contributing)</h2>
<p>
            我们坚信开源社区的力量，并热烈欢迎任何形式的贡献。您的每一个想法、建议或代码提交，都是推动项目前进的宝贵动力。
        </p>
<p>
            如果您对本项目感兴趣，可以通过以下方式参与贡献：
        </p>
<ol>
<li>
<strong>报告问题 (Reporting Bugs)</strong>: 如果您在使用过程中发现了任何错误或不符合预期的行为，请通过GitHub的 <a href="#" target="_blank">Issues</a> 页面提交一个详细的Bug报告。请尽可能提供复现步骤、环境信息和截图。
            </li>
<li>
<strong>提出功能建议 (Feature Requests)</strong>: 如果您有关于新功能或改进现有功能的绝妙想法，也请通过 <a href="#" target="_blank">Issues</a> 页面告诉我们。清晰地描述您希望实现的功能及其应用场景。
            </li>
<li>
<strong>完善文档 (Improving Documentation)</strong>: 一份清晰的文档对项目至关重要。如果您发现文档中有任何错误、遗漏或可以改进的地方（包括本README文件），欢迎提交Pull Request进行修正。
            </li>
<li>
<strong>提交代码 (Submitting Code)</strong>: 这是最直接的贡献方式。我们欢迎您修复Bug、实现新功能或进行代码重构。为保证代码质量和项目风格的统一，请遵循以下流程：
                <ul>
<li>Fork本仓库到您的个人账户。</li>
<li>基于 `main` 分支创建一个新的特性分支 (e.g., `feature/amazing-feature` or `fix/login-bug`)。</li>
<li>在新的分支上进行代码修改。请确保您的代码遵循PEP 8规范，并添加必要的注释。</li>
<li>提交您的修改 (`git commit -m &#39;Add some AmazingFeature&#39;`)。</li>
<li>将您的特性分支推送到您的Fork仓库 (`git push origin feature/AmazingFeature`)。</li>
<li>在GitHub上创建一个Pull Request，目标分支为本仓库的 `main` 分支。请在PR描述中清晰说明您的修改内容和目的。</li>
</ul>
</li>
</ol>
<p>
            在您开始贡献之前，请花些时间阅读我们的 <strong>[CONTRIBUTING.md](CONTRIBUTING.md)</strong> 文件，其中包含了更详细的贡献指南和代码风格规范。
        </p>
<p>
            完毕！
        </p>
<h2 id="section--许可证-license">📄 许可证 (License)</h2>
<p>
            本项目采用 CC-BY-NC 许可证进行分发。这意味着您可以对作品进行复制、分发、展示、表演和演绎创作，但必须为我署名，并且只能将作品用于非商业目的。
        </p>
<p>
            详情请参阅 <strong>[LICENSE](LICENSE)</strong> 文件。
        </p>
